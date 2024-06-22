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
        
        self.application = Application.builder().token(token).build()
        
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.chat))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        user = update.effective_user
        print(user)
        user_auth = self.user_manager.telegram_auth(user.id)
        print(user_auth)
        if user_auth is None:
            user_auth = self.user_manager.register_telegram_user(user.id, user.first_name, user.last_name, user.username)
        print(user_auth)
        
        print(f"user_auth = {user_auth}")
        user_id, thread_id = user_auth
        print(user_id, thread_id)
        self.assistant = FrenAssistant(thread_id)      
        
        await update.message.reply_html(
            rf"Hi {user.mention_html()}!",
            reply_markup=ForceReply(selective=True),
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /help is issued."""
        await update.message.reply_text("Help!")

    async def chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Generate a response from the AI assistant and send it back to the user."""
        if self.assistant is None:
            await update.message.reply_text("Please start the conversation using /start command.")
            return

        user_message = update.message.text
        response = self.assistant.ask_question(user_message)
        await update.message.reply_text(response)

    def run(self):
        """Start the bot."""
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
