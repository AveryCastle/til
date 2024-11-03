import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Install the Slack app and get xoxb- token in advance
SLACK_BOT_TOKEN=os.environ["CHEERY_MATE_SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["CHEERY_MATE_SLACK_APP_TOKEN"]

app = App(token=SLACK_BOT_TOKEN)
 
def get_user_id(email):
    """Fetches the Slack user ID based on the provided employee ID."""
    print("email = {email}")

    try:
        # Use the lookupByEmail method to find the user
        response = app.client.users_lookupByEmail(email=email)
        user_id = response['user']['id']  # Extract user ID from response
        return user_id
        
    except Exception as e:
        print(f"Error fetching user by email '{email}': {e}")
        return None
    
# 각종 이벤트를 annotation 안에 설정하면 된다.
@app.event("message")
@app.event("app_mention")
def conversation(message):    
    conversations_response = app.client.conversations_open(users=message['user'])
    channel_id = conversations_response['channel']['id']
    print(f"channel_id = {channel_id}")
    print(f"user = {message['user']}")

    result = app.client.chat_postMessage(
        channel=channel_id,
        text=f"{message['text']} response",
        as_user=True
    )
    print(result)

def send_direct_message(user_id):
    """Sends a direct message to the specified user."""
    try:
        app.client.chat_postMessage(
            channel=user_id,
            text="안녕? 오늘 하루 힘내!",
            as_user=True
        )
    except Exception as e:
        print(f"Error sending message to user {user_id}: {e}")

if __name__ == '__main__':
    handler = SocketModeHandler(app_token=SLACK_APP_TOKEN, app=app)
    handler.start()
