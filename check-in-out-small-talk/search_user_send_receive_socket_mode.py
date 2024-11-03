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
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('dev-stay-exhibition-conversation')

# 사용자와의 대화 상태 저장
user_conversations = {}

app = App(token=SLACK_BOT_TOKEN)

def fetch_recent_conversation(user_id):
    """Fetches a recent conversation within 5 minutes for the user from DynamoDB."""
    try:
        response = table.get_item(Key={'user_id': user_id})
        if 'Item' in response:
            item = response['Item']
            last_message_time = item['last_message_time']
            if int(time.time()) - last_message_time < timedelta(minutes=5).total_seconds():
                return item['message'], item['conversation_id']  # return conversation history if recent
    except Exception as e:
        logger.error(f"Error fetching conversation for user {user_id}: {e}")
    return []

def store_conversation(user_id, conversation, conversation_id):
    """Stores the conversation in DynamoDB."""
    logger.debug(f"user_id={user_id}, conversation={conversation}, conversation_id={conversation_id}")
    try:
        table.put_item(Item={
                'user_id': user_id,
                'message_count': len(conversation),
                'message': conversation,
                'last_message_time': int(time.time()),
                'conversation_id': conversation_id,
                'event_type': 'check_in',
                'status': 'active'
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

# 각종 이벤트를 annotation 안에 설정하면 된다.
@app.event("message")
@app.event("app_mention")
def conversation(message):
    conversations_response = app.client.conversations_open(users=message['user'])
    channel_id = conversations_response['channel']['id']
    logger.debug(f"channel_id = {channel_id}, user = {message['user']}")

    # Retrieve recent conversation from DynamoDB if within 5 minutes
    user_id = message['user']
    conversation_id = ''
    if user_id not in user_conversations:
        recent_conversation = fetch_recent_conversation(user_id)
        logger.debug(f"recent_conversation={recent_conversation}")
        # recent_conversation의 요소를 처리하는 부분
        if len(recent_conversation) > 0:
            # 각 튜플의 첫 번째 요소에서 메시지와 대화 ID를 가져옵니다.
            for message, conversation_id in recent_conversation:
                logger.debug(f"Message: {message}, Conversation ID: {conversation_id}")
                user_conversations[user_id].append(message)
                conversation_id = conversation_id
        else:
            logger.debug("No recent conversations found.")
            recent_conversation = []
            user_conversations[user_id] = recent_conversation
            conversation_id = generate_conversation_id_with_uuid(user_id)

    logger.debug(f"user_conversations[{user_id}] = {user_conversations[user_id]}")
    # Add current message to conversation
    user_conversations[user_id].append({
        "user": message['text'], 
        "last_message_time": int(time.time())
    })

    # Check conversation limit (5 messages or 5 minutes)
    if len(user_conversations[user_id]) >= 5 or (
        user_conversations[user_id] and
        int(time.time()) - user_conversations[user_id][0]['last_message_time'] > timedelta(minutes=5).total_seconds()
    ):
        store_conversation(user_id, user_conversations[user_id], conversation_id)
        user_conversations.pop(user_id)  # Clear conversation after saving

    system_message = f"{message['text']} response"
    system_time = int(time.time())
    result = app.client.chat_postMessage(
        channel=channel_id,
        text=system_message,
        as_user=True
    )
    user_conversations[user_id].append({
        "system": system_message,
        "last_message_time": system_time  # 시스템 응답에 대해서도 타임스탬프 추가
    })
    logger.debug(f"conversation result = {result}")



if __name__ == '__main__':
    handler = SocketModeHandler(app_token=SLACK_APP_TOKEN, app=app)
    logger.info("Starting Slack Socket Mode handler")
    handler.start()
