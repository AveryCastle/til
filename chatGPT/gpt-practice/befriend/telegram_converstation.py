#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os
import logging
import asyncio

import pytz
from datetime import time, datetime

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply, Update
from telegram.ext import (
  Application, 
  CommandHandler, 
  ContextTypes, 
  ConversationHandler,
  MessageHandler, 
  filters, 
  CallbackContext, 
  JobQueue,
)

from conversation_assistant import FrenAssistant
from smart_greeting_assistant import SmartGreetingAssistant

TOKEN = os.getenv('TELEGRAM_TOKEN')
INACTIVITY_TIMEOUT = 300  # 5분 (300초)
KST = pytz.timezone('Asia/Seoul')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

class TelegramConversation:
    CHOOSING_TIMES, CHOOSING_ACTION, CHATTING = range(3)
    TIME_OPTIONS = [
        "08:00", "08:30", "13:00", "13:30", "17:00",
        "17:30", "18:00", "18:30", "22:00", "22:30"
    ]
    MAX_SELECTIONS = 5

    MESSAGES = {
        'invalid_time': "올바른 시간을 선택해주세요.",
        'already_selected': "이미 선택된 시간입니다. 다른 시간을 선택하거나 '완료'를 눌러주세요.",
        'max_reached': "최대 5개까지만 선택할 수 있습니다. '완료'를 눌러주세요.",
        'time_added': "{}가 추가되었습니다. 현재 선택된 시간: {}\n더 선택하거나 '완료'를 눌러주세요.",
        'choose_action': "시간 설정이 완료되었습니다. 대화를 시작하시겠습니까?",
        'invalid_choice': "올바른 선택지를 골라주세요.",
        'conversation_start': "대화를 시작합니다. 편하게 대화해 주세요. 대화를 끝내려면 /end를 입력하세요.",
        'conversation_end': "대화를 종료합니다. 다음에 또 만나요!"
    }
    
    def __init__(self, user_manager, conversation_manager, token=TOKEN):
        self.user_manager = user_manager
        self.conversation_manager = conversation_manager
        self.assistant = None
        self.user_id = None
        self.thread_id = None
        self.chat_id = None
        self.conversation = []
        self.timeout_task = None  # Task to handle the inactivity timeout
        
        # Create Application with JobQueue
        self.application = Application.builder().token(token).build()
        
        # 시간 설정을 위한 ConversationHandler
        time_setting_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                self.CHOOSING_TIMES: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.choose_times)],
                self.CHOOSING_ACTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.choose_action)],
                self.CHATTING: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.chat),
                    CommandHandler("end", self.end_conversation)
                ],
            },
            fallbacks=[CommandHandler("cancel", self.cancel)],
        )
        
        # 채팅을 위한 ConversationHandler
        chat_handler = ConversationHandler(
            entry_points=[CommandHandler("chat", self.start_conversation)],
            states={
                self.CHATTING: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.chat)],
            },
            fallbacks=[CommandHandler("end", self.end_conversation)],
        )

        self.application.add_handler(time_setting_handler)
        self.application.add_handler(chat_handler)
        
        # Register user message schedules
        self.schedule_user_conversations()


    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Send a message when the command /start is issued."""
        self.initialize_user_info(update)
        
        context.user_data['selected_times'] = []
        
        reply_keyboard = [self.TIME_OPTIONS[i:i+2] for i in range(0, len(self.TIME_OPTIONS), 2)]
        reply_keyboard.append(["완료"])
        
        await update.message.reply_text(
            "안녕하세요! 대화를 나누고싶은 시간을 선택해주세요. 최대 5개까지 선택 가능합니다.\n"
            "선택을 마치면 '완료'를 눌러주세요.",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False),
        )
        return self.CHOOSING_TIMES

    async def initialize_user_info(self, update: Update):
        user = update.effective_user
        self.chat_id = update.message.chat.id
        user_auth = self.user_manager.telegram_auth(user.id)
        if user_auth is None:
            user_auth = self.user_manager.register_telegram_user(user.id, user.first_name, user.last_name, user.username)
        
        self.user_id, self.thread_id = user_auth
        
        self.assistant = FrenAssistant(self.thread_id)
        
        if self.thread_id is None:
            self.thread_id = self.assistant.get_thread_id()
            self.user_manager.update_thread_id(self.user_id, self.thread_id)
            
    async def choose_times(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_choice = update.message.text
        selected_times = context.user_data.get('selected_times', [])

        if user_choice == "완료":
            return await self.done(update, context)

        if not self.is_valid_time(user_choice):
            await update.message.reply_text(self.MESSAGES['invalid_time'])
            return self.CHOOSING_TIMES

        if self.is_already_selected(user_choice, selected_times):
            await update.message.reply_text(self.MESSAGES['already_selected'])
            return self.CHOOSING_TIMES

        if self.is_max_selections_reached(selected_times):
            await update.message.reply_text(self.MESSAGES['max_reached'])
            return self.CHOOSING_TIMES

        self.add_time_to_selections(user_choice, selected_times, context)
        await update.message.reply_text(
            self.MESSAGES['time_added'].format(user_choice, ', '.join(selected_times))
        )

        return self.CHOOSING_TIMES

    def is_valid_time(self, time: str) -> bool:
        return time in self.TIME_OPTIONS

    def is_already_selected(self, time: str, selected_times: list) -> bool:
        return time in selected_times

    def is_max_selections_reached(self, selected_times: list) -> bool:
        return len(selected_times) >= self.MAX_SELECTIONS

    def add_time_to_selections(self, time: str, selected_times: list, context: ContextTypes.DEFAULT_TYPE):
        selected_times.append(time)
        context.user_data['selected_times'] = selected_times
        
    def schedule_user_conversations(self):
        users_by_time = self.user_manager.get_users_by_schedule_time()
        for scheduled_time, user_ids in users_by_time.items():
            for user_id in user_ids:
                logger.debug(f"user {user_id} at {scheduled_time} schedule setting.")
                self._schedule_job(user_id, scheduled_time)

    def schedule_user_conversations_for_user(self, user_id, times):
        for t in times:
            scheduled_time = t.replace(tzinfo=KST)
            self._schedule_job(user_id, scheduled_time)

    def _schedule_job(self, user_id, scheduled_time):
        self.application.job_queue.run_daily(
            self.send_smart_greeting,
            time=scheduled_time,
            days=(0, 1, 2, 3, 4, 5, 6),
            data={'user_id': user_id}
        )
    
    async def choose_action(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_choice = update.message.text

        if user_choice == '대화 시작':
            await update.message.reply_text(
                self.MESSAGES['conversation_start'],
                reply_markup=ReplyKeyboardRemove(),
            )
            return await self.start_conversation(update, context)
        elif user_choice == '종료':
            await update.message.reply_text(
                self.MESSAGES['conversation_end'],
                reply_markup=ReplyKeyboardRemove(),
            )
            return ConversationHandler.END
        else:
            await update.message.reply_text(self.MESSAGES['invalid_choice'])
            return self.CHOOSING_ACTION

    async def start_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if self.assistant is None:
            await self.initialize_user_info(update)
        
        conversation_history, history_thread_id = self.conversation_manager.get_conversations(self.user_id)
        logger.info(f"conversation_history=${conversation_history}, history_thread_id=${history_thread_id}")
        
        smart_greeting_assistant = SmartGreetingAssistant(thread_id=history_thread_id)
        greeting = smart_greeting_assistant.generate_smart_greeting(conversation_history)
        await update.message.reply_text(greeting)
        return self.CHATTING
      
    async def send_smart_greeting(self, context: CallbackContext):
        """Send a smart greeting to all users."""
        telegram_id = context.job.data['user_id']
        user_id = self.user_manager.get_user_id_by_telegram_id(telegram_id)
        logger.info(f"send_smart_greeting scheduleing: telegram_id=${telegram_id}, user_id=${user_id}")
        if user_id:
            conversation_history, history_thread_id = self.conversation_manager.get_conversations(user_id)
            smart_greeting_assistant = SmartGreetingAssistant(thread_id=history_thread_id)
            greeting = smart_greeting_assistant.generate_smart_greeting(conversation_history)
            await context.bot.send_message(chat_id=telegram_id, text=greeting)

    async def chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:        
        """Generate a response from the AI assistant and send it back to the user."""
        if self.assistant is None:
            logger.info("self.assistant is None")
            await self.initialize_user_info(update)

        user_message = update.message.text
        self.conversation.append({'role': 'user', 'message': user_message})

        response = self.assistant.ask_question(user_message)
        self.conversation.append({'role': 'assistant', 'message': response})

        await update.message.reply_text(response)
        
        # Schedule the inactivity timeout
        self.schedule_timeout(context)
        
        return self.CHATTING

    async def end_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """End the conversation and save it to the database."""
        if self.user_id and self.conversation:
            self.conversation_manager.upsert_conversation(self.user_id, self.conversation, self.thread_id)
            self.conversation = []  # Clear the conversation history
            logger.info("Conversation ended and saved.")
            
            if self.timeout_task:
                self.timeout_task.cancel()
        return ConversationHandler.END
          
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.message.reply_text(
            "설정이 취소되었습니다. 기본 시간(오전 9시)으로 설정됩니다.",
            reply_markup=ReplyKeyboardRemove(),
        )
        user_id = update.effective_user.id
        default_time = [time(9, 0)]
        self.user_manager.set_conversation_times(user_id, default_time)
        self.schedule_user_conversations_for_user(user_id, default_time)
        return ConversationHandler.END
    
    async def done(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        user_id = update.effective_user.id
        selected_times = context.user_data.get('selected_times', [])

        if not selected_times:
            selected_times = ["09:00"]  # 기본값: 오전 9시

        times = [datetime.strptime(t, "%H:%M").time() for t in selected_times]
        self.user_manager.set_conversation_times(user_id, times)

        self.schedule_user_conversations_for_user(user_id, times)
        
        await update.message.reply_text(
            f"선택하신 시간: {', '.join(selected_times)}\n"
            f"{self.MESSAGES['choose_action']}",
            reply_markup=ReplyKeyboardMarkup([['대화 시작', '종료']], one_time_keyboard=True),
        )
        return self.CHOOSING_ACTION
    

    async def timeout(self, chat_id):
        """Handle inactivity timeout."""
        if self.user_id and self.conversation:
            self.conversation_manager.upsert_conversation(self.user_id, self.conversation, self.thread_id)
            self.conversation = []  # Clear the conversation history
        logger.info("Conversation ended due to inactivity.")

    def schedule_timeout(self, context: CallbackContext):
        """Schedule a timeout task for inactivity."""
        if self.timeout_task:
            self.timeout_task.cancel()  # Cancel the existing timeout task
        chat_id = context._chat_id
        self.timeout_task = asyncio.create_task(self._timeout_handler(chat_id))

    async def _timeout_handler(self, chat_id):
        """Timeout handler to wait for the inactivity period and then call the timeout function."""
        try:
            await asyncio.sleep(INACTIVITY_TIMEOUT)
            await self.timeout(chat_id)
        except asyncio.CancelledError:
            pass  # Task was cancelled, do nothing

    def run(self):
        """Start the bot."""
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
