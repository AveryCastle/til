import os
import json
import uuid
import time
import boto3
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
client = WebClient(token=SLACK_BOT_TOKEN)

class DatabaseAccess():
    def __init__(self, TABLE_NAME):
        # DynamoDB 세팅
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(TABLE_NAME)

    def get_data_by_user_id(self, user_id):
        res = self.table.get_item(Key={'user_id': user_id})
        if 'Item' in res:
            return res['Item']
        else:
            None
    
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
    email = event['email']
    event_type = event['event_type']

    if event_type == "check_out":
        db_access = DatabaseAccess('dev-stay-exhibition-conversation')
        
        try:
            response = client.users_lookupByEmail(email=email)
            user_id = response['user']['id']
            print(f"found user_id={user_id}")
            found = db_access.get_data_by_user_id(user_id)
            print(f"found user={found}")

            # 첫번째 작별 인사 전달하기
            current_time = int(time.time())
            message = '오늘 일은 잘 마무리했니?' # AI Agent 가 생성해야 함.

            # 사용자에게 대화 시작 메시지 보내기
            result = client.chat_postMessage(
                channel=user_id,
                text=message,
                as_user=True
            )

            print(f"result: {result}")
            system_conversation = found['message']
            system_conversation.append({
                "system": message,
                "last_message_time": current_time
            })
            if result['ok'] == True:
                conversation = {
                        'user_id': user_id,
                        'message_count': 0,
                        'message': system_conversation,
                        'last_message_time': current_time,
                        'conversation_id': generate_conversation_id_with_uuid(user_id),
                        'event_type': event_type,
                        'status': 'active'
                } 
                db_access.put_data(conversation)

        except SlackApiError as e:
            print(f"Error posting message: {e}")

        return {
            "statusCode": 200,
            "body": json.dumps(
                { "message": "goodbye greeting", 
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
