import json
from datetime import datetime, timedelta
import boto3
from boto3.dynamodb.conditions import Key, Attr

# EventBridge 클라이언트 생성
eventbridge = boto3.client('events')

# DynamoDB 클라이언트 생성
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('dev-employee-check-in')

# Lambda Function 클라이언트 생성
lambda_client = boto3.client('lambda')

def update_rule_name(event, rule_name):
    """ rule_name 업데이트하기 """
    email = event['email'] 
    # 조회에 사용할 날짜 추출 (YYYY-MM-DD)
    check_in_day = event['check_in_day']
    
    # 해당 이메일과 날짜로 데이터 조회
    response = table.query(
        KeyConditionExpression=Key('email').eq(email),
        FilterExpression=Attr('check_in_day').eq(check_in_day),
        ProjectionExpression='email, check_in_day'
    )
    
    if not response['Items']:
        print(f"No items found for email: {email} and check_in_day: {check_in_day}")
        return {
            'statusCode': 404,
            'body': f"No records found for email: {event['email']} on date: {check_in_day}"
        }
    
    # 찾은 항목에 대해 rule_name 업데이트
    try:
        update_count = 0
        for item in response['Items']:
            try:
                table.update_item(
                    Key={
                        'email': email
                    },
                    UpdateExpression='SET rule_name = :rule_name',
                    ExpressionAttributeValues={
                        ':rule_name': rule_name
                    }
                )
                update_count += 1
            except Exception as e:
                print(f"Error updating item: {e}")
                continue
        
        print(f"Successfully updated {update_count} items")
        
        return {
            'statusCode': 200,
            'body': {
                'message': 'Successfully updated rule_name',
                'email': email,
                'check_in_day': check_in_day,
                'rule_name': rule_name
            }
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error updating rule_name: {str(e)}"
        }

def get_checkout_localtime_and_utc(input_time, working_hours, hours):
    # 입력된 로컬 시간 기준의 check_in_time을 파싱
    local_time_str = datetime.strptime(input_time, '%Y-%m-%dT%H:%M:%S')
    
    # 근무시간 후의 시간 계산 (로컬시간)
    target_time_kst = local_time_str + timedelta(hours=working_hours)
    
    # UTC로 변환 (로컬시간 - 시간)
    target_time_utc = target_time_kst - timedelta(hours=hours)

    return target_time_kst, target_time_utc

def get_rule_name(email, time_str):
    # email에서 사용자 이름만 추출 (@ 이전 부분)
    username = email.split('@')[0]
    return f"checkout-notification-{username}-{time_str.strftime('%Y%m%d_%H%M%S')}"

def get_schedule_expression_utc(time_utc_str):
    return f"cron({time_utc_str.minute} {time_utc_str.hour} {time_utc_str.day} {time_utc_str.month} ? {time_utc_str.year})"

def get_target_id(email, time_str):
    username = email.split('@')[0]
    return f"checkout-{username}-{time_str.strftime('%Y%m%d_%H%M%S')}"

def lambda_handler(event, context):
    # 0. payload 가져오기
    email = event['email']
    event_type = event['event_type']
    check_in_day = event['check_in_day']
    check_in_time = event['check_in_time']

    # 1. payload 검사하기
    if event_type != "check_out":
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid event type"}),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    # 2. EventBridge 동적으로 생성
    local_checkout_time, checkout_time_utc = get_checkout_localtime_and_utc(check_in_time, 9, 9)

    # 규칙 생성을 위한 고유한 규칙 이름 생성
    rule_name = get_rule_name(email, local_checkout_time)

    # 2-1. EventBridge 규칙 생성 (UTC 기준)
    rule_response = eventbridge.put_rule(
        Name=rule_name,
        # UTC 시간 기준으로 cron 표현식 생성
        ScheduleExpression=get_schedule_expression_utc(checkout_time_utc),
        State='ENABLED',
        Description=f'One-time trigger for {email} Checkout Lambda function'
    )
    print(f"eventbridge rule = {rule_response}")

    # Lambda 함수를 타겟으로 추가
    target_lambda_arn = 'arn:aws:lambda:ap-northeast-2:269388641688:function:dev-stay-exhibition-checkout'

    # 2-2. Lambda 권한 부여 (EventBridge가 Lambda를 호출할 수 있도록)
    try:
        lambda_client.add_permission(
            FunctionName=target_lambda_arn,
            StatementId=f'EventBridge-{rule_name}',
            Action='lambda:InvokeFunction',
            Principal='events.amazonaws.com',
            SourceArn=rule_response['RuleArn']
        )
    except lambda_client.exceptions.ResourceConflictException:
        print(f"Permission already exists for rule: {rule_name}")
        pass
    except Exception as perm_error:
        print(f"Error adding Lambda permission: {str(perm_error)}")
        raise perm_error

    # Target Id 생성
    target_id = get_target_id(email, local_checkout_time)

    payload = {
        "email": email,
        "event_type": "check_out",
        "check_out_time": local_checkout_time.strftime('%Y-%m-%dT%H:%M:%S'),
        "check_out_day": local_checkout_time.strftime('%Y-%m-%d'),
        "rule_name": rule_name,
        "target_id": target_id
    }

    # 2-3. 타겟 추가 (Lambda 함수를 EventBridge 규칙의 타겟으로 설정)
    target_response = eventbridge.put_targets(
        Rule=rule_name,
        Targets=[
            {
                'Id': target_id,
                'Arn': target_lambda_arn,
                'Input': json.dumps(payload)
            }
        ]
    )
    print(f"eventbridge response={target_response}")

    # 타겟 추가 결과 확인
    if target_response['FailedEntryCount'] > 0:
        raise Exception(f"Failed to add target to rule: {target_response['FailedEntries']}")
    
    # 3. DB rule_name 업데이트
    update_result = update_rule_name(event, rule_name)

    # DB Update 실패시 로깅
    if update_result['statusCode'] != 200:
        print(f"rule_name update fail. update_result={update_result}")

    return {
        "statusCode": 200,
        "body": json.dumps(
            { 
                "message": "Checkout EventBridge created", 
                "email": email,
                "check_out_day": local_checkout_time.strftime('%Y-%m-%d'),
                "check_out_time": target_time_kst.strftime('%Y-%m-%dT%H:%M:%S')
            }
        ),
        "headers": {
            "Content-Type": "application/json"
        }
    }
