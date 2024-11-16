import vertexai
from vertexai.generative_models import GenerativeModel, Part

vertexai.init(project="seb-dev-440401", location="asia-northeast3")

images = [
    # "https://dev-image.withinapi.com/373/333/144/dad77a0e8af54bbab60e2d293fa46bb3.jpg", # 외관
    # "https://dev-image.withinapi.com/448/142/257/771f53a82a174302bdb6038b53593cbe.jpg", # 로비
    # "https://image.goodchoice.kr/exhibition/itemContents/a6b561c3bc867d43a03d849d558d09e0.jpg", # 야외수영장
    "https://image.goodchoice.kr/exhibition/itemContents/8d7dc0827fad0a1a81c7b7fa7138b749.jpg", # 야외수영장, 전경
    # "https://image.goodchoice.kr/exhibition/itemContents/b2bc58c319399e0317feeded808faa49.jpg", # 로비
    # "https://image.goodchoice.kr/exhibition/itemContents/64d644a61fd916b6f0c2687dbf5b6316.jpg", # 외관
    # "https://image.goodchoice.kr/exhibition/itemContents/7c1fa1413b977557062f277f2696a6e8.jpg", # 객실
    # "https://image.goodchoice.kr/exhibition/itemContents/b0506b4dda143ed46523c2eaf2bd7d44.jpg", # 객실
    # "https://image.goodchoice.kr/exhibition/itemContents/a0523a9a5e7d6fc0516512f738b4f0a3.jpg", # 객실
    # "https://image.goodchoice.kr/exhibition/itemContents/968f0b48c45768422e046f5a30daf095.jpg", # 레스토랑
    # "https://image.goodchoice.kr/exhibition/itemContents/f4df28f71095ec047ceb5a4df74fb0f5.jpg", # 레스토랑
    "https://image.goodchoice.kr/exhibition/itemContents/6b07bfad8a8dbc56cfc8678c5d2100a5.jpg", # 라운지, 레스토랑
    "https://image.goodchoice.kr/exhibition/itemContents/cdbb0b4daac6cb7858cd0336bf52a522.jpg", # 공용공간, 라운지
    "https://image.goodchoice.kr/exhibition/itemContents/b0fb9f3bda428f5752582c2b53c65cd1.jpg", # 레스토랑, 전경
]


textsi_1 = """
당신은 숙소 관련 이미지 파일이 어떤 category 에 속하는지 분류해야 합니다. 
category 중 가장 적합한 것 1개만 선택해야 합니다. 
특정 category 로 분류하기 불분명할 때는, 즉, 확률이 90퍼센트 미만일 때는, 1순위 category, 2순위 category 를 순서대로 
ambiguous 형식으로 답변합니다.
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

for image in images:
    image_file = Part.from_uri(image, "image/jpeg")
    # Query the model
    response = model.generate_content(
            [image_file, "이 이미지는 어떤 category 인가?"],
            generation_config = generation_config
        )

    print(f"{image} => {response.text}")
