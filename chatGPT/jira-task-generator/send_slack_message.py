import os
import slack_sdk

slack_token = os.environ.get("SLACK_BOT_TOKEN")

client = slack_sdk.WebClient(token=slack_token)

user_id = "avery"
slack_msg = f'<@{user_id}> 파이썬 슬랙 메시지 전송' 

response = client.chat_postMessage(
    channel="slack-msg-test",
    text=slack_msg
)