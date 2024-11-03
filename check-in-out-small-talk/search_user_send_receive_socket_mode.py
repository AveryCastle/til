import os
import logging
from logging.handlers import TimedRotatingFileHandler
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

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

app = App(token=SLACK_BOT_TOKEN)

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

    result = app.client.chat_postMessage(
        channel=channel_id,
        text=f"{message['text']} response",
        as_user=True
    )
    logger.debug(f"conversation result = {result}")

if __name__ == '__main__':
    handler = SocketModeHandler(app_token=SLACK_APP_TOKEN, app=app)
    handler.start()
