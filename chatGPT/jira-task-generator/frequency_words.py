import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from collections import Counter
import re

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)

# Store conversation history
conversation_history = []
# ID of the channel you want to send the message to
channel_id = "C02U3LZ0Y9J"

try:
    # Call the conversations.history method using the WebClient
    # conversations.history returns the first 100 messages by default
    # These results are paginated, see: https://api.slack.com/methods/conversations.history$pagination
    result = client.conversations_history(channel=channel_id, limit=200)

    conversation_history = result["messages"]
    
    # 사용자 정보를 저장할 딕셔너리
    user_info_cache = {}

    # Print results
    logger.info("{} messages found in {}".format(len(conversation_history), channel_id))
    
    for message in reversed(conversation_history):  # 리스트를 뒤집어 최신 메시지를 먼저 출력
        user_id = message.get('user')
        
        # 사용자 정보 캐시에 사용자 정보가 있는지 확인
        if user_id not in user_info_cache:
            user_info_response = client.users_info(user=user_id)
            
            # 사용자 이름을 안전하게 가져오기
            user_name = user_info_response['user'].get('real_name') or user_info_response['user'].get('name') or 'Unknown User'
            user_info_cache[user_id] = user_name
        else:
            user_name = user_info_cache[user_id]
                
        print(f"{user_name} : {message.get('text')}")
    
    
    # 사전에서 텍스트 정보만 추출하여 리스트 생성
    messages = "\n".join([msg['text'] for msg in conversation_history])

    # 사용자 이름 패턴 정의 (예: 'Cinamon / 숙박전시개발팀', 'Ung / 숙박전시개발팀' 등)
    user_pattern = r'\w+ / \w+팀\s*:\s*'

    # 사용자 이름 제외하기
    filtered_messages = re.sub(user_pattern, '', messages)

    # 단어 추출 및 정제
    words = re.findall(r'\b\w+\b', filtered_messages)  # 단어 추출
    words = [word.lower() for word in words]  # 소문자로 변환

    # 단어 빈도 계산
    word_counts = Counter(words)

    # 가장 많이 사용된 단어 10개 추출
    most_common_words = word_counts.most_common(10)

    # 결과 출력
    for word, count in most_common_words:
        print(f"{word}: {count}")

except SlackApiError as e:
    logger.error("Error creating conversation: {}".format(e))
