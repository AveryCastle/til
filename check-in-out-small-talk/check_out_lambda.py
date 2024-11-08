import os
import json
import uuid
import time
import boto3
from boto3.dynamodb.conditions import Key, Attr  # Key와 Attr import 추가
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from database_access import DatabaseAccess, generate_conversation_id_with_uuid

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
client = WebClient(token=SLACK_BOT_TOKEN)

class DatabaseAccess2():
    def __init__(self, TABLE_NAME):
        # DynamoDB 세팅
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(TABLE_NAME)

    def get_data(self, keys):
        res = self.table.get_item(Key=keys)
        if 'Item' in res:
            return res['Item']
        else:
            None

    def query_events_by_attribute(self, key_name, key_value, attribute_name, attribute_value):
        # Query 실행
        response = self.table.query(
            KeyConditionExpression=Key(key_name).eq(key_value),
            FilterExpression=Attr(attribute_name).eq(attribute_value)
        )
        
        # 결과 추출
        items = response.get('Items', [])
        return items
    
    def put_data(self, input_data):
        self.table.put_item(Item =  input_data)
        print("Putting data is completed!")

    def delete_data(self, input_key):
        self.table.delete_item(
            Key = input_key
        )

# def generate_conversation_id_with_uuid(user_id):
#     return f"conv-{user_id}-{uuid.uuid4()}"

def get_message_values(user_id, values): 
    # message 값 추출
    messages = []
    for value in values:
        # event에서 message 가져오기
        message_data = value.get('message', [])
        messages.extend(message_data)  # 메시지 리스트를 messages에 추가  
    return messages

def lambda_handler(event, context):
    email = event['email']
    check_out_day = event['check_out_day']
    check_out_time = event['check_out_time']
    event_type = event['event_type']

    if event_type == "check_out":
        db_access = DatabaseAccess2('dev-stay-exhibition-conversation')
        
        try:
            # 사용자 찾기
            response = client.users_lookupByEmail(email=email)
            user_id = response['user']['id']
            found = db_access.query_events_by_attribute('user_id', user_id, 'event_type', event_type)

            print(f"found user={found}")

            # 첫번째 작별 인사 전달하기
            current_time = int(time.time())
            message = '오늘 일은 잘 마무리했니?' # AI Agent 가 생성해야 함.

            # 사용자에게 대화 시작 메시지 보내기
            response = client.chat_postMessage(
                channel=user_id,
                text=message,
                as_user=True
            )
            print(f"response: {response}")
            
            system_conversation = get_message_values(user_id, found)
            system_conversation.append({
                "system": message,
                "last_message_time": current_time
            })
            if response['ok'] == True:
                conversation = {
                    'user_id': user_id,
                    'event_type': event_type,
                    'conversation_id': generate_conversation_id_with_uuid(user_id),
                    'conversation_day': check_out_day,
                    'message_count': 0,
                    'message': system_conversation,
                    'last_message_time': current_time,
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
