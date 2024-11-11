import json
from datetime import datetime, timedelta
from database_access import DatabaseAccess
import pytz
import boto3

# DB 클라이언트 생성
db_access = DatabaseAccess('dev-employee-check-in')

# Lambda 함수 클라이언트 생성
lambda_client = boto3.client('lambda')

def get_localtime_str(input_time, hours):
    """ 로컬 시간으로 계산하기 """
    utc_now = datetime.now(pytz.UTC)
    print(f"utc_now={utc_now}")

    local_time = utc_now + timedelta(hours=hours)
    local_time_str = input_time or local_time.strftime("%Y-%m-%dT%H:%M:%S")
    local_day_str = datetime.strptime(local_time_str, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d")
    return local_day_str, local_time_str

def lambda_handler(event, context):
    # 0-1. API Gateway 통해서 호출할 때
    print(f"event = ${event}")
    print(f"context = ${context}")
    print(f"body = ${event['body']}")

    body = json.loads(event['body'])
    email = body.get('email')
    event_type = body.get('event_type')
    check_in_time = body.get('check_in_time')

    # 0-2. Lambda 에서 Event Test 할 때 사용
    # email = event['email']
    # event_type = event['event_type']
    # check_in_time = event['check_in_time']

    # 1. event_type 검사
    if event_type != "check_in":
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid event type"}),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    local_check_in_day, local_check_in_time = get_localtime_str(check_in_time, 9)

    # 2. 출근 시간 기록    
    db_access.put_data({
        'email': email,
        'check_in_day': local_check_in_day,
        'check_in_time': local_check_in_time,
        'event_type': event_type
    })

    # 3. Lambda 함수 호출
    # 호출 대상 첫 인사 Lambda 함수의 이름
    first_greeting_target_lambda_function = 'dev-stay-exhibition-first-greeting'
    first_greeting_payload = {
        "email": email,
        "event_type": event_type,
        'check_in_day': local_check_in_day
    }
    # 3-1. 첫 인사 Lambda 함수 호출
    first_greeting_response = lambda_client.invoke(
        FunctionName=first_greeting_target_lambda_function,
        InvocationType='RequestResponse',  # 즉시 호출
        Payload=json.dumps(first_greeting_payload)
    )
    print(f"first_greeting_response= {first_greeting_response}")

    # 3-2. 작별인사 스케쥴링하는 Lambda 함수 호출
    checkout_scheduling_target_lambda_function = 'dev-stay-exhibition-checkout-eventbridge'
    checkout_scheduling_payload = {
        'email': email,
        'check_in_day': local_check_in_day,
        'check_in_time': local_check_in_time,
        'event_type': 'check_out'
    }
    # 다른 Lambda 함수 호출
    checkout_scheduling_response = lambda_client.invoke(
        FunctionName=checkout_scheduling_target_lambda_function,
        InvocationType='RequestResponse',  # 즉시 호출
        Payload=json.dumps(checkout_scheduling_payload)
    )
    print(f"checkout_scheduling_responsee= {checkout_scheduling_response}")
    
    return {
        "statusCode": 200,
        "body": json.dumps(
            { "message": "Check-in processed", 
                "email": email,
                "check_in_day": local_check_in_day,
                "check_in_time": local_check_in_time
            }
        ),
        "headers": {
            "Content-Type": "application/json"
        }
    }
        
