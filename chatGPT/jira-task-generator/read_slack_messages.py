import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

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
    result = client.conversations_history(channel=channel_id, limit=50)

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

except SlackApiError as e:
    logger.error("Error creating conversation: {}".format(e))
