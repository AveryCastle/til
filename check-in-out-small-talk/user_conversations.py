import json
import os
import time
import uuid
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import boto3

# Set up logging
logging.basicConfig(level=logging.INFO)

# Install the Slack app and get xoxb- token in advance
SLACK_BOT_TOKEN=os.environ["SLACK_BOT_TOKEN"]
SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]

MAX_MESSAGES = 5
TIMEOUT = 120  # 2 minutes in seconds for response timeout
LONG_TIMEOUT = 8 * 3600  # 8 hours for resetting the conversation

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('dev-stay-exhibition-conversation')

app = App(token=SLACK_BOT_TOKEN)

handler = SocketModeHandler(app_token=SLACK_APP_TOKEN, app=app)

def get_user_id(email):
    """Fetches the Slack user ID based on the provided employee ID."""
    try:
        # Use the lookupByEmail method to find the user
        response = app.client.users_lookupByEmail(email=email)
        user_id = response['user']['id']  # Extract user ID from response
        return user_id
    except Exception as e:
        print(f"Error fetching user by email '{email}': {e}")
        return None

def generate_conversation_id_with_uuid(user_id):
    return f"conv-{user_id}-{uuid.uuid4()}"

def send_direct_message(user_id, text):
    """Send a direct message to a Slack user."""
    try:
        app.client.chat_postMessage(
            channel=user_id, 
            text=text,
            as_user=True
        )
        return True
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")
        return False

def lambda_handler(event, context):
    try:
        # Lambda 에서 Event Test 할 때 사용
        email = event['email']
        event_type = event['event_type']
        print(f"email = {email}, event_type={event_type}")

        if not email:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'email is required'})
            }
        
        # Get the user_id associated with the email
        user_id = get_user_id(email)

        if not user_id:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User not found'})
            }

        # Check conversation state in DynamoDB
        conversation = table.get_item(Key={'user_id': user_id}).get('Item')
        current_time = int(time.time())
        print(f"conversation={conversation}, current_time={current_time}")

        # Check if we should reset the conversation
        if not conversation or \
            (conversation['event_type'] != event_type) or \
            (current_time - conversation['last_message_time'] > LONG_TIMEOUT):
                # Start a new conversation
                conversation = {
                    'user_id': user_id,
                    'message_count': 0,
                    'message': '',
                    'last_message_time': current_time,
                    'conversation_id': generate_conversation_id_with_uuid(user_id),
                    'event_type': event_type,
                    'status': 'active'
                }
                table.put_item(Item=conversation)
        else:
            # Check if the message count limit or short timeout has been reached
            if conversation['message_count'] < MAX_MESSAGES:
                if current_time - conversation['last_message_time'] > TIMEOUT:
                    return {
                        "statusCode": 200,
                        "body": json.dumps({"status": "Conversation timed out."})
                    }
            else:
                return {
                        "statusCode": 200,
                        "body": json.dumps({"status": "Conversation max count over."})
                }

            # Send message and update conversation state
            message = f"Clock-in confirmed at {current_time}"
            print(f"message = {message}")
            message_sent = send_direct_message(user_id, message)
            if message_sent:
                conversation['message_count'] += 1
                conversation['last_message_time'] = current_time
                conversation['message'] = message
                table.put_item(Item=conversation)

        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': message})
        }
    
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }