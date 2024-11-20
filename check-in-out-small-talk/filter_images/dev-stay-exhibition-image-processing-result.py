import os
import json
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from google.oauth2 import service_account


google_service_account = json.loads(os.getenv('VERTEX_SERVICE_ACCOUNT'))

# credentials 객체 직접 생성
credentials = service_account.Credentials.from_service_account_info(
    google_service_account
)

vertexai.init(project="seb-dev-440401", location="asia-northeast3", service_account=credentials)

textsi_1 = """
우리는 아고다나 booking.com 과 같은 숙소 예약 시스템을 서비스하고 있습니다.
당신은 숙소관련 이미지를 분석하여 적절한 카테고리를 판별하는 AI 에이전트입니다. 주어진 이미지를 분석하여 가장 적합한 카테고리를 식별하고, 정해진 규칙에 따라 결과를 반환해야 합니다.

주요 기능 및 규칙
1. 이미지 분석 시 각 카테고리별 확률을 계산합니다.
결과 반환 규칙:
- 하나의 카테고리가 60% 이상의 확률을 보일 경우: 해당 카테고리만 반환
- 모든 카테고리가 60% 미만일 경우: 상위 2개의 카테고리를 반환
2. 응답 포맷:
- JSON 형식으로 반환
- 카테고리는 자연어로 된 문자열 배열로 제공
- 키 이름은 \"category_type\", \"categories\"를 사용
3. 카테고리
- 외관, 객실, 숙소지도, 공용공간, 전경, 주변, 레스토랑, 라운지, 야외수영장, 실내수영장, 로비, 피트니스


응답 예시
케이스 1: 단일 카테고리 (확률 60% 이상)
json
{
    \"category_type\": \"specific\",
    \"categories\": [\"풍경사진\"]
}
케이스 2: 복수 카테고리 (최고 확률이 60% 미만)
json
{
    \"category_type\": \"anonymous\",
    \"categories\": [\"인물사진\", \"패션사진\"]
}

프로세스 흐름
1. 이미지 수신 및 분석
2. 각 카테고리별 확률 계산
3. 확률에 따른 카테고리 선정
- 최고 확률이 60% 이상: 해당 카테고리만 선정
- 최고 확률이 60% 미만: 상위 2개 카테고리 선정
4. JSON 형식으로 결과 반환

주의사항
1. 확률 계산은 내부적으로만 사용하며, 결과에는 포함하지 않습니다.
2. 카테고리명은 명확하고 이해하기 쉬운 자연어로 표현합니다.
3. 응답은 반드시 지정된 JSON 형식을 따라야 합니다.
4. 불확실한 경우 상위 2개 카테고리를 반환하는 것을 선호합니다.

오류 처리
{
    \"category_type\": \"error\",
    \"message\": \"불분명\"
}

{
    \"category_type\": \"error\",
    \"message\": \"이미지가 주어지지 않았습니다.\"
}
"""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0,
    "top_p": 0.1,
    "response_mime_type": "application/json",
    "response_schema": {"type":"OBJECT","properties":{"category_type":{"type":"STRING","enum":["specific","ambiguous"]},"categories":{"type":"ARRAY","items":{"type":"STRING"}}},"required":["category_type","categories"]},
}


model = GenerativeModel(
    model_name="gemini-1.5-pro-002",
    system_instruction=[textsi_1]
)


def lambda_handler(event, context):
    # TODO implement
    print(f"event={event['Records']}")
    for record in event['Records']:
        print(f'body = {record['body']}')
        body = record['body']
        image = body['image_path']
        image_file = Part.from_uri(image, "image/jpeg")
        # Query the model
        response = model.generate_content(
            [image_file, "이 이미지는 어떤 category 인가?"],
            generation_config = generation_config
        )
        print(f"result = {response}")

    return {
        'statusCode': 200,
        'body': json.dumps(response.candidates[0].content.parts[0].text, ensure_ascii=False)
    }
