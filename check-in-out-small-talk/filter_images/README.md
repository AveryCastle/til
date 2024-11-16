# flow chart
flowchart TB
    subgraph Frontend
        ST[Streamlit UI]
    end

    subgraph Processing
        Lambda1[Lambda\n이미지 분류 실행]
        Lambda2[Lambda\n결과 처리]
        SQS[SQS\n작업 큐]
    end

    subgraph Storage
        S3[(S3\n이미지 저장소)]
        DDB[(DynamoDB\n임시 결과 저장)]
        RDS[(RDS\n최종 DB)]
    end

    subgraph AI
        VM[Vertex AI]
    end

    ST -->|1. 숙소ID 입력| Lambda1
    Lambda1 -->|2. 이미지 정보 조회| S3
    Lambda1 -->|3. 작업 등록| SQS
    SQS -->|4. 배치 처리| Lambda2
    Lambda2 -->|5. 이미지 분석 요청| VM
    VM -->|6. 분석 결과| Lambda2
    Lambda2 -->|7. 임시 저장| DDB
    ST -->|8. 결과 조회| DDB
    ST -->|9. 확정 데이터 저장| RDS