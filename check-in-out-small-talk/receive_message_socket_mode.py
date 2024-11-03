import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from collections import defaultdict
import json
from pathlib import Path
import logging
from typing import Dict

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,  # 디버깅을 위해 DEBUG 레벨로 설정
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ConversationManager:
    def __init__(self, max_conversations: int = 5):
        self.max_conversations = max_conversations
        self.conversation_counts = defaultdict(int)
        self.conversation_file = Path("conversation_counts.json")
        self.load_conversation_counts()

    def load_conversation_counts(self):
        if self.conversation_file.exists():
            with open(self.conversation_file, 'r') as f:
                self.conversation_counts = defaultdict(int, json.load(f))

    def save_conversation_counts(self):
        with open(self.conversation_file, 'w') as f:
            json.dump(dict(self.conversation_counts), f)

    def increment_count(self, user_id: str) -> bool:
        if self.conversation_counts[user_id] >= self.max_conversations:
            return False
        self.conversation_counts[user_id] += 1
        self.save_conversation_counts()
        return True

    def get_remaining_conversations(self, user_id: str) -> int:
        return max(0, self.max_conversations - self.conversation_counts[user_id])

def init_app():
    """앱 초기화 및 설정"""
    try:
        app = App(
            token=os.environ.get("CHEERY_MATE_SLACK_BOT_TOKEN"),
            signing_secret=os.environ.get("CHEERY_MATE_SLACK_SIGNING_SECRET")
        )
        logger.info("Slack app initialized successfully")
        return app
    except Exception as e:
        logger.error(f"Error initializing Slack app: {e}")
        raise

# 앱 초기화
app = init_app()
conversation_manager = ConversationManager()

@app.event("message")
def handle_direct_message(event, say, logger):
    """DM 메시지 처리"""
    try:
        # 이벤트 로깅
        logger.debug(f"Received message event: {event}")
        
        # DM 채널 확인
        if event.get("channel_type") != "im":
            logger.debug("Ignored non-DM message")
            return

        # 봇 메시지 무시
        if event.get("bot_id") or event.get("subtype") == "bot_message":
            logger.debug("Ignored bot message")
            return

        user_id = event.get("user")
        message_text = event.get("text", "").strip()
        
        logger.info(f"Processing DM from user {user_id}: {message_text}")

        # 대화 가능 여부 확인
        remaining = conversation_manager.get_remaining_conversations(user_id)
        
        if remaining <= 0:
            say(text=f"<@{user_id}> 죄송합니다. 대화 횟수 제한(5회)에 도달하였습니다.")
            return

        # 대화 횟수 증가 및 응답
        if conversation_manager.increment_count(user_id):
            response = f"메시지를 받았습니다: '{message_text}'\n남은 대화 횟수: {remaining}회"
            say(text=response)
            logger.info(f"Responded to user {user_id}, remaining conversations: {remaining-1}")
        else:
            say(text=f"<@{user_id}> 죄송합니다. 대화 횟수 제한에 도달하였습니다.")

    except Exception as e:
        logger.error(f"Error handling direct message: {e}", exc_info=True)
        say(text="죄송합니다. 메시지 처리 중 오류가 발생했습니다.")

@app.event("app_mention")
def handle_mention(event, say, logger):
    """앱 멘션 처리"""
    try:
        logger.debug(f"Received mention event: {event}")
        
        user_id = event.get("user")
        mention_text = event.get("text", "").strip()
        
        logger.info(f"Processing mention from user {user_id}: {mention_text}")

        # 대화 가능 여부 확인
        remaining = conversation_manager.get_remaining_conversations(user_id)
        
        if remaining <= 0:
            say(text=f"<@{user_id}> 죄송합니다. 대화 횟수 제한(5회)에 도달하였습니다.")
            return

        # 대화 횟수 증가 및 응답
        if conversation_manager.increment_count(user_id):
            response = f"멘션을 받았습니다: '{mention_text}'\n남은 대화 횟수: {remaining}회"
            say(text=response)
            logger.info(f"Responded to mention from user {user_id}, remaining: {remaining-1}")
        else:
            say(text=f"<@{user_id}> 죄송합니다. 대화 횟수 제한에 도달하였습니다.")

    except Exception as e:
        logger.error(f"Error handling mention: {e}", exc_info=True)
        say(text="죄송합니다. 메시지 처리 중 오류가 발생했습니다.")

# 앱 시작 전 연결 테스트
def test_slack_connection(app):
    """Slack 연결 테스트"""
    try:
        # 봇 정보 가져오기
        auth_test = app.client.auth_test()
        logger.info(f"Bot connected as: {auth_test['bot_id']} in team: {auth_test['team_id']}")
        return True
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False

if __name__ == "__main__":
    try:
        # 환경 변수 확인
        required_env_vars = ["CHEERY_MATE_SLACK_BOT_TOKEN", "CHEERY_MATE_SLACK_APP_TOKEN", "CHEERY_MATE_SLACK_SIGNING_SECRET"]
        missing_vars = [var for var in required_env_vars if not os.getenv(var)]
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

        # 연결 테스트
        if not test_slack_connection(app):
            raise ConnectionError("Failed to connect to Slack")

        # Socket Mode 핸들러 초기화 및 시작
        handler = SocketModeHandler(
            app=app,
            app_token=os.environ["CHEERY_MATE_SLACK_APP_TOKEN"]
        )
        
        logger.info("Starting Slack app in Socket Mode...")
        handler.start()
        
    except Exception as e:
        logger.error(f"Failed to start app: {e}", exc_info=True)
        raise