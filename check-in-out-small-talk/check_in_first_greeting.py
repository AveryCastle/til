import os
import json
import uuid
import time
import boto3
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from database_access import DatabaseAccess, generate_conversation_id_with_uuid

# Slack 클라이언트 생성
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
slack_client = WebClient(token=SLACK_BOT_TOKEN)

# DynamoDB 클라이언트 생성
db_access = DatabaseAccess('dev-stay-exhibition-conversation')

def lambda_handler(event, context):
    email = event['email']
    event_type = event['event_type']
    check_in_day = event['check_in_day']

    if event_type != "check_in":
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid event type"}),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    try:
        response = slack_client.users_lookupByEmail(email=email)
        user_id = response['user']['id']

        # 1. LLM 통해 첫번째 인사말 전달하기
        current_time = int(time.time())
        message = '안녕? 출근길 어땠어?' # AI Agent 가 생성해야 함.

        # 2. 사용자에게 대화 시작 메시지 보내기
        result = slack_client.chat_postMessage(
            channel=user_id,
            text=message,
            as_user=True
        )
        print(f"result: {result}")

        # 3. 시스템 메세지 저장하기
        system_conversation = []
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
                    'conversation_day': check_in_day,
                    'event_type': event_type,
                    'status': 'active'
            } 
            db_access.put_data(conversation)

    except SlackApiError as e:
        print(f"Error posting message: {e}")

    return {
        "statusCode": 200,
        "body": json.dumps(
            { 
                "message": "first greeting", 
                "email": email
            }
        ),
        "headers": {
            "Content-Type": "application/json"
        }
    }
