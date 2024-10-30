import json
from datetime import datetime, timedelta
import boto3


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
        self.table.put_item(
            Item =  input_data
        )
        print("Putting data is completed!")

    def delete_data(self, input_key):
        self.table.delete_item(
            Key = input_key
        )

def lambda_handler(event, context):
    # Gateway 통해서 POST Method 로 요청할 때 사용
    # print(f"event = ${event}")
    # print(f"context = ${context}")
    # print(f"body = ${event['body']}")

    # body = json.loads(event['body'])
    # employee_id = body.get('employee_id')
    # event_type = body.get('event_type')

    # Lambda 에서 Event Test 할 때 사용
    employee_id = event['employee_id']
    event_type = event['event_type']
    check_in_time = event['check_in_time']
    
    utc_now = datetime.utcnow()

    # utc+9
    korea_time = utc_now + timedelta(hours=9)
    check_in_time = check_in_time or korea_time.strftime("%Y-%m-%dT%H:%M:%S")


    if event_type == "check_in":
        db_access = DatabaseAccess('dev-employee-check-in')

        # 출근 시간 기록
        db_access.delete_data({
            'employee_id': employee_id
        })
    
        db_access.put_data({
            'employee_id': employee_id,
            'check_in_time': check_in_time,
            'message_count': 0
        })
        
        # Slack 메시지 전송 등의 로직 수행
        
        return {
            "statusCode": 200,
            "body": json.dumps(
                { "message": "Check-in processed", 
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
