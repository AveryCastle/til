import os
import json
import logging
import uuid
from datetime import datetime, timedelta
import time
import boto3
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
client = WebClient(token=SLACK_BOT_TOKEN)

# Set up logging
logging.basicConfig(level=logging.INFO)

class DatabaseAccess():
    def __init__(self, TABLE_NAME):
        # DynamoDB 세팅
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(TABLE_NAME)
    
    def get_data(self):
        res = self.table.scan()
        items = res['Items'] # 모든 item
        count = res['Count'] # item 개수
        return items, count
    
    def put_data(self, input_data):
        self.table.put_item(Item =  input_data)
        print("Putting data is completed!")

    def delete_data(self, input_key):
        self.table.delete_item(
            Key = input_key
        )

def generate_conversation_id_with_uuid(user_id):
    return f"conv-{user_id}-{uuid.uuid4()}"

def lambda_handler(event, context):
    # print(f"event = ${event}")
    # print(f"context = ${context}")
    # print(f"body = ${event['body']}")

    # body = json.loads(event['body'])
    # email = body.get('email')
    # event_type = body.get('event_type')
    # check_in_time = body.get('check_in_time')

    # Lambda 에서 Event Test 할 때 사용
    email = event['email']
    event_type = event['event_type']

    if event_type == "check_in":
        db_access = DatabaseAccess('dev-stay-exhibition-conversation')

        try:
            response = client.users_lookupByEmail(email=email)
            user_id = response['user']['id']

            # 첫번째 인사말 전달하기
            current_time = int(time.time())
            message = '안녕? 출근 잘 했어?' # AI Agent 가 생성해야 함.

            # 사용자에게 대화 시작 메시지 보내기
            result = client.chat_postMessage(
                channel=user_id,
                text=message,
                as_user=True
            )

            print(f"result: {result}")

            conversation = {
                    'user_id': user_id,
                    'message_count': 0,
                    'message': message,
                    'last_message_time': current_time,
                    'conversation_id': generate_conversation_id_with_uuid(user_id),
                    'event_type': event_type,
                    'status': 'active'
            } 
            db_access.put_data(Item = conversation)

        except SlackApiError as e:
            print(f"Error posting message: {e}")

        return {
            "statusCode": 200,
            "body": json.dumps(
                { "message": "first greeting", 
                  "email": email
                }
            ),
            "headers": {
                "Content-Type": "application/json"
            }
        }
    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid event type"}),
            "headers": {
                "Content-Type": "application/json"
            }
        }
