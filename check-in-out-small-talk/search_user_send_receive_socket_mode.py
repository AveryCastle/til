import os
import logging
from logging.handlers import TimedRotatingFileHandler
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from datetime import datetime, timedelta
import time
import boto3
import uuid

# 로그 파일 경로 설정
log_directory = "blackhole/log"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)  # 디렉토리가 없으면 생성합니다.

log_file_path = os.path.join(log_directory, "app.log")

# 루트 로거 설정
logging.basicConfig(level=logging.DEBUG)  # 루트 로거에 기본 레벨 설정
logger = logging.getLogger()  # 루트 로거 가져오기

# 날짜별 로그 파일 핸들러 설정 (매일 자정에 로그 파일을 새로 생성)
handler = TimedRotatingFileHandler(
    log_file_path,
    when="midnight",
    interval=1,
    backupCount=7  # 최근 7일치 로그 파일을 보관
)
handler.suffix = "%Y-%m-%d"  # 로그 파일에 날짜 포맷 추가
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# 기존에 핸들러가 붙어 있을 수 있으므로 핸들러를 모두 제거하고 새로 추가
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(handler)

# Slack 앱 초기화
SLACK_BOT_TOKEN = os.environ["CHEERY_MATE_SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["CHEERY_MATE_SLACK_APP_TOKEN"]

# DynamoDB setup
dynamodb = boto3.resource('dynamodb', region_name = 'ap-northeast-2')
table = dynamodb.Table('dev-stay-exhibition-conversation')

# 사용자와의 대화 상태 저장
all_conversations = {}

app = App(token=SLACK_BOT_TOKEN)

def fetch_recent_messages(user_id):
    """Fetches a recent conversation within 5 minutes for the user from DynamoDB."""
    try:
        response = table.get_item(Key={'user_id': user_id})
        if 'Item' in response:
            item = response['Item']
            last_message_time = item['last_message_time']
            if int(time.time()) - last_message_time < timedelta(minutes=5).total_seconds():
                logger.debug(f"Data found. item['message']={item['message']}, conversation_id={item['conversation_id']}, item['status']={item['status']}")
                return item['message'], item['conversation_id'], item['status']  # return conversation history if recent
    except Exception as e:
        logger.error(f"Error fetching conversation for user {user_id}: {e}")
    return [], None, None

def store_conversation(user_id, conversations, conversation_id):
    """Stores the conversation in DynamoDB."""
    logger.debug(f"save converations. user_id={user_id}, conversations={conversations}, conversation_id={conversation_id}")
    try:
        table.put_item(Item={
                'user_id': user_id,
                'message_count': get_user_message_count(user_id),
                'message': conversations,
                'last_message_time': int(time.time()),
                'conversation_id': conversation_id,
                'event_type': 'check_in',
                'status': 'limit'
        })
    except Exception as e:
        logger.error(f"Error storing conversation for user {user_id}: {e}")

def generate_conversation_id_with_uuid(user_id):
    return f"conv-{user_id}-{uuid.uuid4()}"

def get_user_id(email):
    """Fetches the Slack user ID based on the provided employee ID."""
    logger.debug(f"email = {email}")

    try:
        # Use the lookupByEmail method to find the user
        response = app.client.users_lookupByEmail(email=email)
        user_id = response['user']['id']  # Extract user ID from response
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
        bool: True if the user has more than five messages, False otherwise.
    """
    if user_id in all_conversations:
        conversations = all_conversations[user_id]
        # 'user' 키가 있는 데이터만 필터링하여 개수를 셉니다.
        user_conversation_count = sum(1 for user_conversation in conversations['messages'] if 'user' in user_conversation)
        return user_conversation_count
    return 0

def add_message(conversations, user_id, message):
    """
    Adds a user conversation to the all_conversations object.

    Args:
        conversations (dict): The dictionary storing all conversations.
        user_id (str): The ID of the user.
        conversation (dict): The conversation data to add.

    Returns:
        None
    """
    if user_id in conversations:
        conversations[user_id]["messages"].append(message)
    else:
        conversations[user_id]["messages"] = { "messages": [message] }



# 각종 이벤트를 annotation 안에 설정하면 된다.
@app.event("message")
@app.event("app_mention")
def conversation(message):
    conversations_response = app.client.conversations_open(users=message['user'])
    channel_id = conversations_response['channel']['id']
    logger.debug(f"channel_id = {channel_id}, user_id = {message['user']}")

    # Retrieve recent conversation from DynamoDB if within 5 minutes
    user_id = message['user']
    if user_id not in all_conversations:
        recent_messages, conversation_id, status = fetch_recent_messages(user_id)
        if status == 'limit':
            return
        
        # recent_messages 의 요소를 처리하는 부분
        if len(recent_messages) > 0:
            # 각 튜플의 첫 번째 요소에서 메시지와 대화 ID를 가져옵니다.
            for recent_message in recent_messages:
                all_conversations[user_id] = { 
                    "messages": [ recent_message ],
                    "conversation_id": conversation_id
                }
        else:
            recent_messages = []
            conversation_id = generate_conversation_id_with_uuid(user_id)
            logger.debug(f"No recent conversations found. so setting conversation id = {conversation_id}")
            all_conversations[user_id] = { "messages": [], "conversation_id" : conversation_id }

    logger.debug(f"After fetching user info. Conversation_id = {all_conversations[user_id]['conversation_id']}, Message = {message}")

    # Add current message to conversation as user
    user_message_info = {
        "user": message['text'], 
        "last_message_time": int(time.time())
    }
    add_message(all_conversations, user_id, user_message_info)

    # Check conversation limit (5 messages or 5 minutes)
    if get_user_message_count(user_id) > 5 or (
        all_conversations[user_id] and
        int(time.time()) - all_conversations[user_id]["messages"][len(all_conversations[user_id]["messages"])-1]['last_message_time'] > timedelta(minutes=5).total_seconds()
    ):
        store_conversation(user_id, all_conversations[user_id]["messages"], all_conversations[user_id]["conversation_id"])
        all_conversations.pop(user_id)  # Clear conversation after saving
        return

    # Send system message and save it in user_conversations.
    system_message = f"{message['text']} response"
    system_time = int(time.time())
    result = app.client.chat_postMessage(
        channel=channel_id,
        text=system_message,
        as_user=True
    )

    if result['ok'] == True:
        system_message_info = {
            "system": system_message,
            "last_message_time": system_time  # 시스템 응답에 대해서도 타임스탬프 추가
        }
        add_message(all_conversations, user_id, system_message_info)
    else:
        logger.error(f"result = {result}")

if __name__ == '__main__':
    handler = SocketModeHandler(app_token=SLACK_APP_TOKEN, app=app)
    logger.info("Starting Slack Socket Mode handler")
    handler.start()
