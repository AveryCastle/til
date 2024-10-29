import json
from datetime import datetime, timedelta

def lambda_handler(event, context):
    print(f"event = ${event}")
    print(f"context = ${context}")
    print(f"body = ${event['body']}")

    body = json.loads(event['body'])
    employee_id = body.get('employee_id')
    event_type = body.get('event_type')

    utc_now = datetime.now(datetime.timezone.utc)

    # utc+9
    korea_time = utc_now + timedelta(hours=9)
    check_in_time = body.get('check_in_time') or korea_time.isoformat()

    # Lambda 에서 Event Test 할 때 사용
    # employee_id = event['employee_id']
    # event_type = event['event_type']

    
    if event_type == "check_in":
        # 출근 시간 기록 및 Slack 메시지 전송 등의 로직 수행
        # ...
        
        return {
            "statusCode": 200,
            "body": json.dumps(
                { 
                    "message": "Check-in processed", 
                    "employee_id": employee_id,
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
