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

import re
from datetime import time, datetime

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext, JobQueue

from conversation_assistant import FrenAssistant
from smart_greeting_assistant import SmartGreetingAssistant

TOKEN = os.getenv('TELEGRAM_TOKEN')
INACTIVITY_TIMEOUT = 60  # 1분 (60초)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

class TelegramConversation:
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
        
         # 정기적인 메시지 전송 설정
        job_queue = self.application.job_queue
        job_queue.run_daily(self.send_smart_greeting, time=time(9, 0), days=(0, 1, 2, 3, 4, 5, 6))
        job_queue.run_daily(self.send_smart_greeting, time=time(13, 0), days=(0, 1, 2, 3, 4, 5, 6))
        job_queue.run_daily(self.send_smart_greeting, time=time(18, 0), days=(0, 1, 2, 3, 4, 5, 6))
        job_queue.run_daily(self.send_smart_greeting, time=time(21, 0), days=(0, 1, 2, 3, 4, 5, 6))
        
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("set_times", self.set_message_times))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("end", self.end_conversation))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.chat))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        self.chat_id = update.message.chat.id
        print(f"chat_id = {self.chat_id}")
        user_auth = self.user_manager.telegram_auth(user.id)
        if user_auth is None:
            user_auth = self.user_manager.register_telegram_user(user.id, user.first_name, user.last_name, user.username)
        
        self.user_id, self.thread_id = user_auth
        
        self.assistant = FrenAssistant(self.thread_id)
        
        if self.thread_id is None:
            self.thread_id = self.assistant.get_thread_id()
            self.user_manager.update_thread_id(self.user_id, self.thread_id)
        
        conversation_history, history_thread_id = self.conversation_manager.get_conversations(self.user_id)
        logging.info(f"conversation_history={conversation_history}")
        
        smartGreetingAssistant = SmartGreetingAssistant(thread_id=history_thread_id)
        greeting = smartGreetingAssistant.generate_smart_greeting(conversation_history)

        await update.message.reply_html(greeting)
        self.conversation.append({'role': 'assistant', 'message': greeting})
        
        # Schedule the inactivity timeout
        self.schedule_timeout(context)

    async def set_message_times(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_id = update.effective_user.id
        message = update.message.text.split(maxsplit=1)
        
        if len(message) == 1:
            await update.message.reply_text("시간을 입력해주세요. 예: /set_times 09:00 13:00 17:30")
            return

        times = message[1].split()
        if len(times) > 5:
            await update.message.reply_text("최대 5개의 시간만 설정할 수 있습니다.")
            return

        valid_times = []
        for t in times:
            if re.match(r'^\d{2}:\d{2}$', t):
                try:
                    valid_time = datetime.strptime(t, "%H:%M").time()
                    valid_times.append(valid_time)
                except ValueError:
                    await update.message.reply_text(f"잘못된 시간 형식입니다: {t}")
                    return
            else:
                await update.message.reply_text(f"잘못된 시간 형식입니다: {t}")
                return

        if not valid_times:
            valid_times = [time(9, 0)]  # 기본값: 오전 9시

        self.user_manager.set_message_times(user_id, valid_times)
        
        await update.message.reply_text("메시지 수신 시간이 설정되었습니다.")
        self.__schedule_user_messages__(user_id, valid_times)
        
    def __schedule_user_messages__(self, user_id, times):
        for t in times:
            self.application.job_queue.run_daily(
                self.send_smart_greeting,
                time=t,
                days=(0, 1, 2, 3, 4, 5, 6),
                context={'user_id': user_id}
            )
    
    async def send_smart_greeting(self, context: CallbackContext):
        """Send a smart greeting to all users."""
        users = self.user_manager.get_telegram_users()  # 모든 사용자 가져오기
        for user in users:
            user_id, thread_id, telegram_id, first_name, last_name, username = user
            print(f"User ID: {user_id}, Thread ID: {thread_id}, Telegram ID: {telegram_id}, Name: {first_name} {last_name}, Username: {username}")
            conversation_history, history_thread_id = self.conversation_manager.get_conversations(user_id)
            
            smartGreetingAssistant = SmartGreetingAssistant(thread_id=history_thread_id)
            greeting = smartGreetingAssistant.generate_smart_greeting(conversation_history)
            
            await context.bot.send_message(chat_id=telegram_id, text=greeting)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_text("Help!")

    async def chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:        
        """Generate a response from the AI assistant and send it back to the user."""
        if self.assistant is None:
            # await update.message.reply_text("Please start the conversation using /start command.")
            await self.start(update, context)
            return

        user_message = update.message.text
        self.conversation.append({'role': 'user', 'message': user_message})

        response = self.assistant.ask_question(user_message)
        self.conversation.append({'role': 'assistant', 'message': response})

        await update.message.reply_text(response)
        
        # Schedule the inactivity timeout
        self.schedule_timeout(context)

    async def end_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """End the conversation and save it to the database."""
        if self.user_id and self.conversation:
            self.conversation_manager.upsert_conversation(self.user_id, self.conversation, self.thread_id)
            self.conversation = []  # Clear the conversation history
            await update.message.reply_text("Conversation ended and saved.")
            
            if self.timeout_task:
                self.timeout_task.cancel()

    async def timeout(self, chat_id):
        """Handle inactivity timeout."""
        if self.user_id and self.conversation:
            self.conversation_manager.upsert_conversation(self.user_id, self.conversation, self.thread_id)
            self.conversation = []  # Clear the conversation history
        print(f"chat_id = {chat_id}")
        await self.application.bot.send_message(chat_id, "Conversation ended due to inactivity.")

    def schedule_timeout(self, context: CallbackContext):
        """Schedule a timeout task for inactivity."""
        if self.timeout_task:
            self.timeout_task.cancel()  # Cancel the existing timeout task
        chat_id = context._chat_id
        print(f"chat_id = {chat_id}")
        self.timeout_task = asyncio.create_task(self._timeout_handler(chat_id))

    async def _timeout_handler(self, chat_id):
        """Timeout handler to wait for the inactivity period and then call the timeout function."""
        try:
            print(f"chat_id = {chat_id}")
            await asyncio.sleep(INACTIVITY_TIMEOUT)
            await self.timeout(chat_id)
        except asyncio.CancelledError:
            pass  # Task was cancelled, do nothing

            
    def run(self):
        """Start the bot."""
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
