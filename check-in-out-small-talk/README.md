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
                    "employee_id": "emp12345",
                    "event_type": "check_in",
                    "check_in_time": "2024-10-30T08:00:05.935774"
                    }'

                curl -X POST https://3fnd0mpvr7.execute-api.ap-northeast-2.amazonaws.com/dev/checkIn \
                -H "Content-Type: application/json" \
                -d '{
                    "employee_id": "emp12345",
                    "event_type": "check_in"
                    }'
            ```
2. Lambda Function
    2.1 dev-stay-platform-checkIn-gateway
