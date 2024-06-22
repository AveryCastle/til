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

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from conversation_assistant import FrenAssistant
from smart_greeting_assistant import SmartGreetingAssistant

TOKEN = os.getenv('TELEGRAM_TOKEN')

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
        self.conversation = []
        
        self.application = Application.builder().token(token).build()
        
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("end", self.end_conversation))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.chat))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        user_auth = self.user_manager.telegram_auth(user.id)
        if user_auth is None:
            user_auth = self.user_manager.register_telegram_user(user.id, user.first_name, user.last_name, user.username)
        
        self.user_id, self.thread_id = user_auth
        
        self.assistant = FrenAssistant(self.thread_id)
        
        if self.thread_id is None:
            self.thread_id = self.assistant.get_thread_id()
            self.user_manager.update_thread_id(self.user_id, self.thread_id)
        
        conversation_history, history_thread_id = self.conversation_manager.get_conversations(self.user_id)
        logging.info(f"conversation_history={conversation_history}, history_thread_id={history_thread_id}")
        
        smartGreetingAssistant = SmartGreetingAssistant(thread_id=history_thread_id)
        greeting = smartGreetingAssistant.generate_smart_greeting(conversation_history)

        await update.message.reply_html(greeting)
        self.conversation.append({'role': 'assistant', 'message': greeting})


    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_text("Help!")

    async def chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Generate a response from the AI assistant and send it back to the user."""
        if self.assistant is None:
            await update.message.reply_text("Please start the conversation using /start command.")
            return

        user_message = update.message.text
        self.conversation.append({'role': 'user', 'message': user_message})

        response = self.assistant.ask_question(user_message)
        self.conversation.append({'role': 'assistant', 'message': response})

        await update.message.reply_text(response)

    async def end_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """End the conversation and save it to the database."""
        if self.user_id and self.conversation:
            self.conversation_manager.upsert_conversation(self.user_id, self.conversation, self.thread_id)
            await update.message.reply_text("Conversation ended and saved.")
            self.conversation = []  # Clear the conversation history
            
    def run(self):
        """Start the bot."""
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
