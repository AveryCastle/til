mport os
from fastapi import FastAPI, Request, HTTPException
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from collections import defaultdict
import json
from pathlib import Path
import hmac
import hashlib
import time
from typing import Dict, Any
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class SlackEventHandler:
    def __init__(self, slack_token: str, signing_secret: str):
        self.client = WebClient(token=slack_token)
        self.signing_secret = signing_secret
        self.conversation_counts = defaultdict(int)
        self.max_conversations = 5
        self.conversation_file = Path("conversation_counts.json")
        self.load_conversation_counts()
        
        # 봇 ID 가져오기
        try:
            self.bot_id = self.client.auth_test()["bot_id"]
            self.bot_user_id = self.client.auth_test()["user_id"]
            logger.info(f"Bot initialized with ID: {self.bot_id} and user ID: {self.bot_user_id}")
        except SlackApiError as e:
            logger.error(f"Error getting bot info: {e.response['error']}")
            raise

    def load_conversation_counts(self):
        """저장된 대화 기록을 불러옵니다."""
        if self.conversation_file.exists():
            with open(self.conversation_file, 'r') as f:
                self.conversation_counts = defaultdict(int, json.load(f))

    def save_conversation_counts(self):
        """대화 기록을 파일에 저장합니다."""
        with open(self.conversation_file, 'w') as f:
            json.dump(dict(self.conversation_counts), f)

    def verify_slack_request(self, timestamp: str, signature: str, body: bytes) -> bool:
        """Slack 요청의 유효성을 검증합니다."""
        if not timestamp or not signature:
            return False
        
        basestring = f"v0:{timestamp}:{body.decode()}"
        my_signature = f"v0={hmac.new(self.signing_secret.encode(), basestring.encode(), hashlib.sha256).hexdigest()}"
        return hmac.compare_digest(my_signature, signature)

    async def handle_message(self, event_data: Dict[str, Any]):
        """메시지 이벤트를 처리합니다."""
        try:
            # 이벤트 데이터 로깅
            logger.info(f"Received event data: {event_data}")
            
            # 기본 정보 추출
            user_id = event_data.get('user')
            channel = event_data.get('channel')
            text = event_data.get('text', '').strip()
            event_type = event_data.get('type')
            subtype = event_data.get('subtype')

            # 자신의 메시지는 무시
            if user_id == self.bot_user_id:
                return

            # 봇 멘션 확인
            is_bot_mentioned = f"<@{self.bot_user_id}>" in text
            
            # 봇이 멘션되지 않았다면 무시
            if not is_bot_mentioned:
                logger.info("Bot was not mentioned, ignoring message")
                return

            logger.info(f"Processing message from user {user_id} in channel {channel}")

            # 대화 횟수 확인
            if self.conversation_counts[user_id] >= self.max_conversations:
                try:
                    await self._send_message(
                        channel,
                        f"<@{user_id}> 죄송합니다. 대화 횟수 제한({self.max_conversations}회)에 도달하였습니다. 다음 기회에 다시 이용해주세요."
                    )
                except SlackApiError as e:
                    logger.error(f"Error sending limit message: {e.response['error']}")
                return

            # 대화 처리 및 응답
            clean_text = text.replace(f"<@{self.bot_user_id}>", "").strip()
            response_text = f"<@{user_id}> 메시지를 받았습니다: '{clean_text}'\n남은 대화 횟수: {self.max_conversations - self.conversation_counts[user_id]}회"
            
            await self._send_message(channel, response_text)
            
            # 대화 횟수 증가 및 저장
            self.conversation_counts[user_id] += 1
            self.save_conversation_counts()
            logger.info(f"Updated conversation count for user {user_id}: {self.conversation_counts[user_id]}")

        except Exception as e:
            logger.error(f"Error handling message: {str(e)}", exc_info=True)

    async def _send_message(self, channel: str, text: str):
        """메시지 전송을 담당하는 헬퍼 메서드"""
        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=text
            )
            logger.info(f"Message sent successfully to channel {channel}")
            return response
        except SlackApiError as e:
            logger.error(f"Error sending message: {e.response['error']}")
            raise

    def get_remaining_conversations(self, user_id: str) -> int:
        """사용자의 남은 대화 가능 횟수를 반환합니다."""
        return max(0, self.max_conversations - self.conversation_counts[user_id])

# 환경 변수에서 토큰 가져오기
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")

if not SLACK_TOKEN or not SLACK_SIGNING_SECRET:
    raise ValueError("SLACK_BOT_TOKEN and SLACK_SIGNING_SECRET must be set in environment variables")

# SlackEventHandler 인스턴스 생성
slack_handler = SlackEventHandler(SLACK_TOKEN, SLACK_SIGNING_SECRET)

@app.post("/slack/events")
async def slack_events(request: Request):
    """Slack 이벤트를 처리하는 엔드포인트"""
    try:
        # 요청 바디 가져오기
        body = await request.body()
        
        # 요청 로깅
        logger.info(f"Received request to /slack/events")
        logger.debug(f"Request body: {body.decode()}")
        
        # Slack 요청 검증
        timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
        signature = request.headers.get("X-Slack-Signature", "")
        
        # 타임스탬프 검증 (5분 이상 지난 요청 거부)
        if abs(time.time() - int(timestamp)) > 60 * 5:
            logger.warning("Received request with expired timestamp")
            raise HTTPException(status_code=400, detail="Invalid timestamp")
        
        # 서명 검증
        if not slack_handler.verify_slack_request(timestamp, signature, body):
            logger.warning("Received request with invalid signature")
            raise HTTPException(status_code=400, detail="Invalid signature")

        # 이벤트 데이터 파싱
        event_data = json.loads(body)
        
        # URL 검증 응답
        if event_data.get("type") == "url_verification":
            logger.info("Responding to URL verification challenge")
            return {"challenge": event_data.get("challenge")}
        
        # 이벤트 처리
        if event_data.get("type") == "event_callback":
            event = event_data.get("event", {})
            if event.get("type") == "message":
                await slack_handler.handle_message(event)
        
        return {"ok": True}
    
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {str(e)}")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
