import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Install the Slack app and get xoxb- token in advance
SLACK_BOT_TOKEN=os.environ["CHEERY_MATE_SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["CHEERY_MATE_SLACK_APP_TOKEN"]
print(f"SLACK_BOT_TOKEN={SLACK_BOT_TOKEN}")
print(f"SLACK_APP_TOKEN={SLACK_APP_TOKEN}")

 
app = App(token=SLACK_BOT_TOKEN)
 
# 각종 이벤트를 annotation 안에 설정하면 된다.
@app.event("message")
@app.event("app_mention")
def dm(message):
    print(f"message = {message}")
    print(f"user = {message['user']}")
    
    conversations_response = app.client.conversations_open(users=message['user'])
    channel_id = conversations_response['channel']['id']
    print(f"channel_id = {channel_id}")

    result = app.client.chat_postMessage(
        channel=channel_id,
        text="나랑 있는 채널로 해야 하는데...나랑만 대화를 해야해...",
        as_user=True
    )
    print(result)

if __name__ == '__main__':
    handler = SocketModeHandler(app_token=SLACK_APP_TOKEN, app=app)
    handler.start()
