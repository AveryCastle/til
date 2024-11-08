import os
import logging
from logging.handlers import TimedRotatingFileHandler
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime, timedelta
import time
import boto3
import uuid

# Constants
LOG_DIR = "blackhole/log"
CONVERSATION_TABLE_NAME = "dev-stay-exhibition-conversation"
SLACK_BOT_TOKEN = os.environ["CHEERY_MATE_SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["CHEERY_MATE_SLACK_APP_TOKEN"]
MESSAGE_LIMIT = 5
TIME_LIMIT = 300  # 5 minutes

# Setup logging
os.makedirs(LOG_DIR, exist_ok=True)
log_file_path = os.path.join(LOG_DIR, "app.log")
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = TimedRotatingFileHandler(
    log_file_path,
    when="midnight",
    interval=1,
    backupCount=7
)
handler.suffix = "%Y-%m-%d"
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(handler)

# Initialize Slack app
slack_app = App(token=SLACK_BOT_TOKEN)

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-2')
conversation_table = dynamodb.Table(CONVERSATION_TABLE_NAME)

# Dictionary to store user conversations
all_conversations = {}

def fetch_recent_messages(user_id):
    """Fetches a recent conversation within 5 minutes for the user from DynamoDB."""
    try:
        response = conversation_table.get_item(Key={'user_id': user_id})
        if 'Item' in response:
            item = response['Item']
            last_message_time = item['last_message_time']
            if int(time.time()) - last_message_time < TIME_LIMIT:
                logger.debug(f"Data found. item['message']={item['message']}, conversation_id={item['conversation_id']}, item['status']={item['status']}")
                return item['message'], item['conversation_id'], item['status']
    except Exception as e:
        logger.error(f"Error fetching conversation for user {user_id}: {e}")
    return [], None, None

def store_conversation(user_id, conversations, conversation_id):
    """Stores the conversation in DynamoDB."""
    logger.debug(f"Saving conversation. user_id={user_id}, conversations={conversations}, conversation_id={conversation_id}")
    try:
        now = time.time()
        conversation_table.put_item(Item={
            'user_id': user_id,
            'message_count': get_user_message_count(user_id),
            'message': conversations,
            'last_message_time': int(now),
            'conversation_id': conversation_id,
            'conversation_day': datetime.fromtimestamp(now).strftime('%Y-%m-%d'),
            'event_type': 'check_in',
            'status': 'limit'
        })
    except Exception as e:
        logger.error(f"Error storing conversation for user {user_id}: {e}")

def generate_conversation_id(user_id):
    return f"conv-{user_id}-{uuid.uuid4()}"

def get_korean_date(utc_time):    
    # UTC 시간을 한국 시간(KST)으로 변환 (UTC + 9 시간 차이)
    korean_time = datetime.fromtimestamp(utc_time) + timedelta(hours=9)
    logger.debug(f"korean_time={korean_time}")
    # 한국 시간을 'yyyy-mm-dd' 형식으로 반환
    return korean_time.strftime('%Y-%m-%d')

def get_user_id(email):
    """Fetches the Slack user ID based on the provided email."""
    logger.debug(f"email = {email}")
    try:
        response = slack_app.client.users_lookupByEmail(email=email)
        user_id = response['user']['id']
        return user_id
    except Exception as e:
        logger.error(f"Error fetching user by email '{email}': {e}")
        return None

def get_user_message_count(user_id):
    """
    Checks if the user has more than five messages under the 'user' key in all_conversations.

    Args:
        user_id (str): The ID of the user.

    Returns:
        int: The number of user messages.
    """
    if user_id in all_conversations:
        conversations = all_conversations[user_id]["messages"]
        user_message_count = sum(1 for message in conversations if 'user' in message)
        return user_message_count
    return 0

def add_message(conversations, user_id, message):
    """
    Adds a user conversation to the all_conversations object.

    Args:
        conversations (dict): The dictionary storing all conversations.
        user_id (str): The ID of the user.
        message (dict): The conversation data to add.

    Returns:
        None
    """
    if user_id in conversations:
        conversations[user_id]["messages"].append(message)
    else:
        conversations[user_id] = {"messages": [message]}

@slack_app.event("message")
@slack_app.event("app_mention")
def handle_conversation(message):
    user_id = message['user']
    channel_id = get_conversation_channel(user_id)
    recent_messages, conversation_id, status = fetch_recent_messages(user_id)

    if status == 'limit':
        return

    initialize_conversation(user_id, recent_messages, conversation_id)
    add_user_message(user_id, message['text'])
    check_and_store_conversation(user_id)
    send_system_message(channel_id, user_id, message['text'])

def initialize_conversation(user_id, recent_messages, conversation_id):
    if user_id not in all_conversations:
        if recent_messages:
            all_conversations[user_id] = {"messages": recent_messages, "conversation_id": conversation_id}
        else:
            conversation_id = generate_conversation_id(user_id)
            logger.debug(f"No recent conversations found. Setting conversation id = {conversation_id}")
            all_conversations[user_id] = {"messages": [], "conversation_id": conversation_id}

def add_user_message(user_id, message_text):
    user_message = {
        "user": message_text,
        "last_message_time": int(time.time())
    }
    add_message(all_conversations, user_id, user_message)

def check_and_store_conversation(user_id):
    if get_user_message_count(user_id) > MESSAGE_LIMIT or (
        all_conversations[user_id]["messages"] and
        int(time.time()) - all_conversations[user_id]["messages"][-1]['last_message_time'] > TIME_LIMIT
    ):
        store_conversation(
            user_id,
            all_conversations[user_id]["messages"],
            all_conversations[user_id]["conversation_id"]
        )
        all_conversations.pop(user_id)  # Clear conversation after saving

def send_system_message(channel_id, user_id, user_message):
    system_message = f"{user_message} response"
    system_time = int(time.time())
    result = slack_app.client.chat_postMessage(
        channel=channel_id,
        text=system_message,
        as_user=True
    )

    if result['ok']:
        system_message_info = {
            "system": system_message,
            "last_message_time": system_time
        }
        add_message(all_conversations, user_id, system_message_info)
    else:
        logger.error(f"Error sending system message: {result}")

def get_conversation_channel(user_id):
    """Fetches the conversation channel ID for the given user."""
    try:
        conversations_response = slack_app.client.conversations_open(users=user_id)
        channel_id = conversations_response['channel']['id']
        return channel_id
    except Exception as e:
        logger.error(f"Error getting conversation channel for user {user_id}: {e}")
        return None

if __name__ == '__main__':
    handler = SocketModeHandler(app_token=SLACK_APP_TOKEN, app=slack_app)
    logger.info("Starting Slack Socket Mode handler")
    handler.start()