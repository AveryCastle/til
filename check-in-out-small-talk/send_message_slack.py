import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("CHEERY_MATE_SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)

# ID of the channel you want to send the message to
channel_id = "D07V8JNPNM6"

try:
    # Call the chat.postMessage method using the WebClient
    result = client.chat_postMessage(
        channel=channel_id, 
        text="Hello world",
        as_user=True
    )
    logger.info(result)

except SlackApiError as e:
    logger.error(f"Error posting message: {e}")