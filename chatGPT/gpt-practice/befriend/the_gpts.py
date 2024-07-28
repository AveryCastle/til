#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

import os
import logging
import re

from telegram import ForceReply, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, ConversationHandler, filters
import requests
import json

# Telegram Token
TOKEN = os.getenv('TELEGRAM_LAAS_TOKEN')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

url = "https://api-laas.wanted.co.kr/api/preset/v2/chat/completions"

headers = {
    "accept": "application/json",
    "project": "PROMPTHON_PRJ_431",
    "apiKey": "79922959a824374c0e44c26e5d8dcee536842a4b279c196a1e4deb30f012829a",
    "Content-Type": "application/json"
}

payload_template = {
    "hash": "7705c62829e4a28c7dfdf5da1a8eaac8e96adefa32b3f53057e9372200727268",
    "params": {
        "task_assigned": "",
        "task_history": "",
        "assignee": ""
    },
    "model": "HCX-003",
    "messages": [
        {
            "role": "user",
            "content": ""
        }
    ]
}

# Define conversation states
CHOOSING, TYPING_REPLY = range(2)

reply_keyboard = [
    ['담당자 찾기', '관련업무 찾기', '담당자 업무찾기'],
]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def filtered_user_input(user_input):
    payload = payload_template.copy()
    # Process the input
    for pattern, key in patterns.items():
        match = re.search(pattern, user_input)
        if match:
            value = user_input[match.end():].strip()
            payload['params'][key] = value
            payload['messages'][0]['content'] = f"{key} has been set to {value}"
            break  # Assuming only one pattern is matched at a time
    
    return payload

def update_payload(payload, **kwargs):
    # Valid fields
    valid_fields = ["task_assigned", "task_history", "assignee"]
    
    # Update the fields in the payload
    for field, value in kwargs.items():
        if field in valid_fields:
            payload['params'][field] = value
        else:
            raise ValueError(f"Invalid field: {field}. Must be one of {valid_fields}")
    
    # Update the messages content with the user's input
    updated_fields = ', '.join([f"{field} has been set to {value}" for field, value in kwargs.items() if field in valid_fields])
    payload['messages'][0]['content'] = updated_fields
    
    return payload

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "안녕하세요! 무엇을 도와드릴까요?",
        reply_markup=markup,
    )
    return CHOOSING

async def choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    logger.info("User %s chose %s", user.first_name, update.message.text)
    context.user_data['choice'] = update.message.text
    await update.message.reply_text(
        f"{update.message.text}에 대한 질문을 입력해 주세요.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return TYPING_REPLY

async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    text = update.message.text
    choice = context.user_data['choice']
    logger.info("User %s's choice: %s, input: %s", user.first_name, choice, text)

    if choice == '담당자 찾기':
        payload_field = "task_assigned"
    elif choice == '관련업무 찾기':
        payload_field = "task_history"
    else:
        payload_field = "assignee"

    payload = update_payload(payload_template.copy(), **{payload_field: text})
    response = requests.post(url, headers=headers, data=json.dumps(payload)).json()

    await update.message.reply_text(response['choices'][0]['message']['content'])
    return ConversationHandler.END

def main() -> None:    
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex('^(담당자 찾기|관련업무 찾기|담당자 업무찾기)$'), choice
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex('^Done$')), received_information
                )
            ],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
