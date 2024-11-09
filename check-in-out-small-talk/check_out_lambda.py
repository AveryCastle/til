import os
import json
import time
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from database_access import DatabaseAccess, generate_conversation_id_with_uuid
import boto3

# Slack 클라이언트 생성
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
slack_client = WebClient(token=SLACK_BOT_TOKEN)

# DynamoDB 클라이언트 생성
conversation_db = DatabaseAccess('dev-stay-exhibition-conversation')

# EventBridge 클라이언트 생성
eventbridge = boto3.client('events')

def get_message_values(values): 
    # message 값 추출
    messages = []
    for value in values:
        # event에서 message 가져오기
        message_data = value.get('message', [])
        messages.extend(message_data)  # 메시지 리스트를 messages에 추가  
    return messages

def delete_eventbridge_rule(rule_name, target_id):
    try:
        # 1. rule에 연결된 target을 삭제 (Lambda 함수는 삭제되지 않습니다)
        eventbridge.remove_targets(
            Rule = rule_name,
            Ids = [target_id]
        )
        print(f"Target(s) for rule '{rule_name}' have been removed.")

        # 2. rule 삭제
        eventbridge.delete_rule(
            Name=rule_name
        )
        print(f"EventBridge rule '{rule_name}', target id '{target_id}' has been deleted.")
    
    except Exception as e:
        print(f"Error: {e}")
        pass

def lambda_handler(event, context):
    # 0. payload 가져오기
    email = event['email']
    check_out_day = event['check_out_day']
    check_out_time = event['check_out_time']
    event_type = event['event_type']
    rule_name = event['rule_name']
    target_id = event['target_id']

    # 1. payload 검사하기
    if event_type != "check_out":
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid event type"}),
            "headers": {
                "Content-Type": "application/json"
            }
        }
        
    try:
        # 2. 사용자 찾기
        response = slack_client.users_lookupByEmail(email=email)
        user_id = response['user']['id']
        found = conversation_db.query_events_by_attribute('user_id', user_id, 'event_type', event_type)
        print(f"found user={found}")

        # 3. LLM 연동하여 첫번째 작별 인사 전달하기
        current_time = int(time.time())
        message = '오늘 일 잘 마무리했니?' # AI Agent 가 생성해야 함.

        # 4. 사용자에게 대화 시작 메시지 보내기
        response = slack_client.chat_postMessage(
            channel=user_id,
            text=message,
            as_user=True
        )
        print(f"response: {response}")
        
        if response['ok'] == True:
            conversations = get_message_values(found)
            conversations.append({
                "system": message,
                "last_message_time": current_time
            })

            # 5. DB 에 Message 반영하기
            conversation = {
                'user_id': user_id,
                'event_type': event_type,
                'conversation_id': generate_conversation_id_with_uuid(user_id),
                'conversation_day': check_out_day,
                'message_count': 0,
                'message': conversations,
                'last_message_time': current_time,
                'status': 'active'
            } 
            conversation_db.put_data(conversation)

            # 6. EventBridge Rule 삭제하기
            delete_eventbridge_rule(rule_name, target_id)

    except SlackApiError as e:
        print(f"Error posting message: {e}")

    return {
        "statusCode": 200,
        "body": json.dumps(
            { 
                "message": "goodbye greeting", 
                "email": email
            }
        ),
        "headers": {
            "Content-Type": "application/json"
        }
    }
        
