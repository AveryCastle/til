import os
import json
import logging
from datetime import datetime, timedelta
import boto3

# Set up logging
logging.basicConfig(level=logging.INFO)

lambda_client = boto3.client('lambda')

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
    check_in_time = event['check_in_time']

    utc_now = datetime.utcnow()

    # utc+9
    korea_time = utc_now #+ timedelta(hours=9)
    check_in_time = check_in_time or korea_time.strftime("%Y-%m-%dT%H:%M:%S")
    check_in_day = datetime.strptime(check_in_time, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
    print(f"check_in_time = {check_in_time}")

    if event_type == "check_in":
        db_access = DatabaseAccess('dev-employee-check-in')

        # 출근 시간 기록    
        db_access.put_data({
            'email': email,
            'check_in_time': check_in_time,
            'check_in_day': check_in_day,
            'event_type': event
        })

        # 다른 람다 함수 호출
        # 호출할 대상 Lambda 함수의 이름 - 첫 인사
        target_lambda_function_name1 = 'dev-stay-exhibition-first-greeting'
        
        payload1 = {
            "email": email,
            "event_type": event_type,
            'check_in_day': check_in_day
        }

         # 다른 Lambda 함수 호출
        response = lambda_client.invoke(
            FunctionName=target_lambda_function_name1,
            InvocationType='RequestResponse',  # 즉시 호출
            Payload=json.dumps(payload1)
        )

        # 호출 결과를 읽기
        response_payload = json.loads(response['Payload'].read())       
        print(f"response_payload= {response_payload}")

        # 호출할 대상 Lambda 함수의 이름 - 작별 인사
        target_lambda_function_name2 = 'dev-stay-exhibition-checkout-eventbridge'

        payload2 = {
            'email': email,
            'check_in_time': check_in_time,
            'check_in_day': check_in_day,
            'event_type': 'check_out'
        }

        # 다른 Lambda 함수 호출
        response2 = lambda_client.invoke(
            FunctionName=target_lambda_function_name2,
            InvocationType='RequestResponse',  # 즉시 호출
            Payload=json.dumps(payload2)
        )

        print(f"response event-bridge= {response2}")
        
        return {
            "statusCode": 200,
            "body": json.dumps(
                { "message": "Check-in processed", 
                  "email": email,
                  "check_in_day": check_in_day,
                  "check_in_time": check_in_time
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
