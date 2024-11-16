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
당신은 숙소 관련 이미지 파일이 어떤 category 에 속하는지 분류해야 합니다. 
category 중 가장 적합한 것 1개만 선택해야 합니다. 
특정 category 로 분류하기 불분명할 때는, 즉, 확률이 70퍼센트 미만일 때는, ambiguous 형식으로 답변합니다.
ambiguous 형식은 가장 높은 확률의 카테고리부터 적은 확률의 카테고리 순으로 최대 2개만 선택합니다.
example 을 참고해주세요.

<category>
외관, 객실, 숙소지도, 공용공간, 전경, 주변, 레스토랑, 라운지, 야외수영장, 실내수영장, 로비, 피트니스
</category> 

<ambiguous>
{
    "category_type": "ambiguous",
    "categories": ["1순위 카테고리", "2순위 카테고리"]
}
</ambiguous>

<example>
1. 분명하게 특정 category에 속하는 경우
case1.
{
    "category_type": "specific",
    "categories": ["객실"]
}

case2.
{
    "category_type": "specific",
    "categories": ["외관"]
}

case3.
{
    "category_type": "specific",
    "categories": ["주변"]
}

case4.
{
    "category_type": "specific",
    "categories": ["야외수영장"]
}

2. 불분명한 category에 속하는 경우
case1.
{
    "category_type": "ambiguous",
    "categories": ["야외수영장", "전경"]
}

case2.
{
    "category_type": "ambiguous",
    "categories": ["로비", "공용공간"]
}

case3.
{
    "category_type": "ambiguous",
    "categories": ["전경", "주변"]
}
</example>"""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
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
        'body': json.dumps('Hello from Lambda!')
    }
