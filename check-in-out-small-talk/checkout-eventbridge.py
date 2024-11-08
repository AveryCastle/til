import json
from database_access import DatabaseAccess, generate_conversation_id_with_uuid
from datetime import datetime, timedelta
import pytz
import boto3


def lambda_handler(event, context):
    # Lambda 에서 Event Test 할 때 사용
    email = event['email']
    event_type = event['event_type']
    check_in_day = event['check_in_day']
    check_in_time = event['check_in_time']

    utc_now = datetime.utcnow()

    if event_type == "check_out":
        db_access = DatabaseAccess('dev-employee-check-in')

        # EventBridge 클라이언트 생성
        eventbridge = boto3.client('events')

        # 호출에 사용할 payload (event)
        # check_in_time이 문자열이므로 datetime 객체로 변환
        check_in_datetime = datetime.strptime(check_in_time, "%Y-%m-%dT%H:%M:%S")
        # 9시간 추가
        check_out_time = check_in_datetime + timedelta(hours=9)
        # 결과를 문자열로 변환
        check_out_time_str = check_out_time.strftime("%Y-%m-%dT%H:%M:%S")
        
        
        # email에서 사용자 이름만 추출 (@ 이전 부분)
        username = email.split('@')[0]

        # EventBridge 규칙 생성을 위한 데이터 준비
        # UTC 시간으로 변환
        utc_time = check_out_time.astimezone(pytz.UTC)

        rule_name = f"checkout-notification-{username}-{check_out_time.strftime("%Y-%m-%d.%H-%M-%S")}"
    
        # 이벤트 규칙 생성
        response = eventbridge.put_rule(
            Name=rule_name,
            ScheduleExpression=f"cron({check_out_time.minute} {check_out_time.hour} {check_out_time.day} {check_out_time.month} ? {check_out_time.year})",
            State='ENABLED',
            Description=f'Checkout notification for {email}'
        )
        print(f"eventbridge rule = {response}")

        # 퇴근 알림 Lambda를 타겟으로 설정
        payload = {
            "email": email,
            "event_type": "check_out",
            "check_out_time": check_out_time_str,
            "check_out_day": check_out_time.strftime("%Y-%m-%d")
        }

        # Target Id 및 Lambda Function ARN
        target_id = f"{username}-checkout-{check_out_time.strftime('%Y-%m-%d.%H-%M-%S')}"
        target_lambda_arn = "arn:aws:lambda:ap-northeast-2:269388641688:function:dev-stay-exhibition-checkout"

        response = eventbridge.put_targets(
            Rule=rule_name,
            Targets=[
                {
                    'Id': target_id,
                    'Arn': target_lambda_arn,
                    'Input': json.dumps(payload)
                }
            ]
        )
        print(f"eventbridge response={response}")

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            response = db_access.put_data({
                'email': email,
                'check_in_day':  check_in_day,
                'rule_name': rule_name
            })
            print(f"database response={response}")
        
        return {
            "statusCode": 200,
            "body": json.dumps(
                { "message": "Check-out processed", 
                  "email": email,
                  "check_out_day": check_in_day,
                  "check_out_time": check_out_time_str
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
