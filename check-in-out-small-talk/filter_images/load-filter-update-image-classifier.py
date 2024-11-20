import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part
import json
import os
import logging
import pymysql
import boto3
from botocore.exceptions import ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Environment variables
DB_HOST = 'with-yeogi-rds-read.abouthere.kr'#os.environ['DB_HOST']
DB_NAME = 'yeogi' # os.environ['DB_NAME']
DB_USER = 'within_dev'# 'within_dev' # 'yeogi' #os.environ['DB_USER']
DB_PASSWORD = 'With!n@()' #'With!n@()' # 'DQlapaTm&79()' #os.environ['DB_PASSWORD']

vertexai.init(project="seb-dev-440401", location="asia-northeast3")

images = [
    "https://dev-image.withinapi.com/373/333/144/dad77a0e8af54bbab60e2d293fa46bb3.jpg", # 외관
    "https://dev-image.withinapi.com/448/142/257/771f53a82a174302bdb6038b53593cbe.jpg", # 로비
    "https://image.goodchoice.kr/exhibition/itemContents/a6b561c3bc867d43a03d849d558d09e0.jpg", # 야외수영장
    "https://image.goodchoice.kr/exhibition/itemContents/8d7dc0827fad0a1a81c7b7fa7138b749.jpg", # 야외수영장, 전경
    "https://image.goodchoice.kr/exhibition/itemContents/b2bc58c319399e0317feeded808faa49.jpg", # 로비
    "https://image.goodchoice.kr/exhibition/itemContents/64d644a61fd916b6f0c2687dbf5b6316.jpg", # 외관
    "https://image.goodchoice.kr/exhibition/itemContents/7c1fa1413b977557062f277f2696a6e8.jpg", # 객실
    "https://image.goodchoice.kr/exhibition/itemContents/b0506b4dda143ed46523c2eaf2bd7d44.jpg", # 객실
    "https://image.goodchoice.kr/exhibition/itemContents/a0523a9a5e7d6fc0516512f738b4f0a3.jpg", # 객실
    "https://image.goodchoice.kr/exhibition/itemContents/968f0b48c45768422e046f5a30daf095.jpg", # 레스토랑
    "https://image.goodchoice.kr/exhibition/itemContents/f4df28f71095ec047ceb5a4df74fb0f5.jpg", # 레스토랑
    "https://image.goodchoice.kr/exhibition/itemContents/6b07bfad8a8dbc56cfc8678c5d2100a5.jpg", # 라운지, 레스토랑
    "https://image.goodchoice.kr/exhibition/itemContents/cdbb0b4daac6cb7858cd0336bf52a522.jpg", # 공용공간, 라운지
    "https://image.goodchoice.kr/exhibition/itemContents/b0fb9f3bda428f5752582c2b53c65cd1.jpg", # 레스토랑, 전경
]

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
- 키 이름은 categories, code, name, accuracy를 사용
3. 카테고리
 [name]:[code]
- 외관: APPEARANCE
- 객실: ROOM
- 숙소지도: SITEMAP
- 공용공간: PUBLIC_AREA
- 전경: VIEW
- 주변: SURROUNDING
- 레스토랑: RESTAURANT
- 라운지: LOUNGE
- 야외수영장: OUTDOOR_POOL
- 실내수영장: INDOOR_POOL
- 로비: LOBBY
- 피트니스: FITNESS

응답 예시
케이스 1: 단일 카테고리 (확률 60% 이상)
json
{
    \"accurcy\": 99.91,
    \"categories\": [
        {
            \"code\": \"SURROUNDING\",
            \"name\": \"주변\"
        }
    ]
}
케이스 2: 복수 카테고리 (최고 확률이 60% 미만)
json
{
    \"accurcy\": 55.17,
    \"categories\": [
        {
            \"code\": \"ROOM\",
            \"name\": \"객실\"
        },
        {
            \"code\": \"PUBLIC_AREA\",
            \"name\": \"공용공간\"
        }
    ]
}

프로세스 흐름
1. 이미지 수신 및 분석
2. 각 카테고리별 확률 계산
3. 확률에 따른 카테고리 선정
- 최고 확률이 60% 이상: 해당 카테고리만 선정
- 최고 확률이 60% 미만: 상위 2개 카테고리 선정
4. 확률이 60% 미만일 때, 상위 1번째 확률에 대해 accuracy 에 표시
5. JSON 형식으로 결과 반환

주의사항
1. 확률 계산은 내부적으로만 사용하며, 결과에는 포함하지 않습니다.
2. 카테고리 이름과 코드는 `3. 카테고리` 에 있는 정보만 활용한다.
3. 응답은 반드시 지정된 JSON 형식을 따라야 합니다.
4. 불확실한 경우 상위 2개 카테고리를 반환하는 것을 선호합니다.

오류 처리
{
    \"accuracy\": 0.0,
    \"message\": \"불분명\"
}

{
    \"accuracy\": 0.0,
    \"message\": \"이미지가 주어지지 않았습니다.\"
}
"""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 0,
    "top_p": 0,
    "response_mime_type": "application/json",
    "response_schema": {"type":"OBJECT","properties":{"accuracy":{"type":"NUMBER"},"categories":{"type":"ARRAY","items":{"type":"OBJECT","properties":{"code":{"type":"STRING"},"name":{"type":"STRING"}},"required":["code","name"]}}},"required":["accuracy","categories"]},
}

safety_settings = [
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
    SafetySetting(
        category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=SafetySetting.HarmBlockThreshold.OFF
    ),
]


model = GenerativeModel(
    model_name="gemini-1.5-pro-002",
    system_instruction=[textsi_1]
)

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            db=DB_NAME,
            connect_timeout=5,
            read_timeout=60,
            write_timeout=60,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except pymysql.Error as e:
        logger.error(f"Failed to connect to database: {str(e)}")
        raise

def get_property_images(property_seq):
    """Fetch property images from database"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT
                    pi.property_seq,
                    pi.property_image_seq,
                    pi.image_seq,
                    CONCAT('https://dev-image.withinapi.com', '', ti.path, '/', ti.file_name, '.', ti.mime_type) as image_path
                 FROM tb_property_image pi
                INNER JOIN tb_image ti ON pi.image_seq = ti.image_seq
                WHERE 1=1
                  AND pi.property_seq = %s
                  AND pi.image_type = 'HOTEL_AFFILIATE'
             ORDER BY pi.image_sort
            """
            cursor.execute(query, (property_seq,))
            return cursor.fetchall()
    except pymysql.Error as e:
        logger.error(f"Database query failed: {str(e)}")
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    property_ids = [6674] #[76065, 6674]

    for property_id in property_ids:
        property_images = get_property_images(property_id)
        
        # Extract image_path and property_seq
        result = [
            {"property_seq": property_image["property_seq"], "image_path": property_image["image_path"]}
            for property_image in property_images
        ]

        for property_image in result:
            image_path = property_image['image_path']
            image_file = Part.from_uri(image_path, "image/jpeg")
            logger.debug(f"image_file={image_file}")
            # Query the model
            response = model.generate_content(
                    [image_file, "이 이미지는 어떤 category 인가?"],
                    generation_config = generation_config,
                    safety_settings=safety_settings,
                )

            print(f"{image_path} => {json.dumps(response.candidates[0].content.parts[0].text, ensure_ascii=False)}")
