[Dev AWS 환경]
1. GATEWAY NAME: dev-stay-platform-checkIn-gateway
    1.1 Resources
        1.1.1 GET / 
        1.1.2 POST /checkIn
            1.1.2.1 예시
            ```
                curl -X POST https://3fnd0mpvr7.execute-api.ap-northeast-2.amazonaws.com/dev/checkIn \
                -H "Content-Type: application/json" \
                -d '{
                        "email": "avery@gccompany.co.kr",
                        "event_type": "check_in",
                        "check_in_time": "2024-11-03T07:50:05"
                    }'
            ```
2. Lambda Function
    2.1 dev-stay-platform-checkIn-gateway
        - 사용자가 출석 체크를 하면 체크인을 하기 위해 DB 에 출근시간을 기록하고, dev-stay-exhibition-first-greeting 를 호출한다.
        - Lambda Function 을 만든 IAM Role 에서 DBPut, DBDelete, DBGet 할 수 있는 권한이 있는지 확인해야 한다.
    2.2 dev-stay-exhibition-first-greeting
        - 사용자가 출석 체크를 하면 처음으로 사용자에게 보낼 메세지를 생성하여 사용자에게 슬랙으로 발송한다.

3. DynamoDB Name
3.1 dev-employee-check-in
    - partition_key: employee_id
    - schema
        email(string)
        check_in_time(string)
        event_type(string)
        event_rule_name(string)
3.2 dev-stay-exhibition-conversation
    - partition_key: user_id
    - schema
        user_id(string)
        conversation_id(string)
        event_type(string)
        last_message_time(int)
        message(string)
        message_count(int)
        status(active)

4. EC2
    4.1 D-avery-chat-ec2-001
    - Socket Mode 로 사용자와 대화를 나누는 서버이다.
    - Private IP: 200.0.100.137
    - ``` ssh -i devwithincokr.pem  ec2-user@200.0.100.137 ```