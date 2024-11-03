import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Install the Slack app and get xoxb- token in advance
SLACK_BOT_TOKEN=os.environ["CHEERY_MATE_SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["CHEERY_MATE_SLACK_APP_TOKEN"]
print(f"SLACK_BOT_TOKEN={SLACK_BOT_TOKEN}")
print(f"SLACK_APP_TOKEN={SLACK_APP_TOKEN}")

app = App(token=SLACK_BOT_TOKEN)

# Dictionary to track user conversations
user_conversations = {}

@app.command("/hello-socket-mode")
def hello_command(ack, body):
    user_id = body["user_id"]
    ack(f"Hi, <@{user_id}>!")

@app.event("app_mention")
def event_test(say, body):
    user_id = body["user"]
    
    # Initialize conversation count if not present
    if user_id not in user_conversations:
        user_conversations[user_id] = 0

    # Respond to the user
    if user_conversations[user_id] < 5:
        user_conversations[user_id] += 1
        say(f"Hi there! This is message number {user_conversations[user_id]} for you.")
    else:
        say("We've reached the maximum number of exchanges. Thank you!")

@app.event("app_mention")
@app.event("")
@app.event("message")  # Listen for all message events, including DMs
def handle_message(event, say):
    logging.info("event=", event)
    logging.info("event=", say)

    user_id = event["user"]
    
    # Ignore messages sent by the bot itself to avoid loops
    if user_id == app.bot_user_id:
        return

    # Check if the message is a DM
    if event.get("channel_type") == "im":  # "im" indicates a direct message
        if user_id not in user_conversations:
            user_conversations[user_id] = 0
        
        # Respond to the user
        if user_conversations[user_id] < 5:
            user_conversations[user_id] += 1
            say(f"This is your DM message number {user_conversations[user_id]}.")
        else:
            say("We've reached the maximum number of exchanges. Thank you!")            

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()