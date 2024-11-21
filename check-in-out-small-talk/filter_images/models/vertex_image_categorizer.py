import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part
import json

# vertexai.init(project="seb-dev-440401", location="asia-northeast3")
class VertexImageCategorizer:
    def __init__(self, 
                 project_id, 
                 location="asia-northeast3", 
                 model_name="gemini-1.5-pro-002"):
        """
        Initialize the image categorization service.
        
        :param project_id: Google Cloud project ID
        :param location: Google Cloud region (default: asia-northeast3)
        :param model_name: Vertex AI model to use (default: gemini-1.5-pro-002)
        """
        # System instruction for image categorization
        self.system_instruction = """
우리는 아고다나 booking.com 과 같은 숙소 예약 시스템을 서비스하고 있습니다.
당신은 숙소관련 이미지를 분석하여 적절한 카테고리를 판별하는 AI 에이전트입니다. 주어진 이미지를 분석하여 가장 적합한 카테고리를 식별하고, 정해진 규칙에 따라 결과를 반환해야 합니다.

주요 기능 및 규칙
1. 이미지 분석 시 각 카테고리별 확률(accuracy)을 계산합니다.
결과 반환 규칙:
- 하나의 카테고리가 60% 이상의 확률(accuracy)을 보일 경우: 해당 카테고리만 반환
- 최고 확률(accuracy)의 카테고리가 60% 미만일 경우: 상위 2개의 카테고리를 반환
- 이미지가 모든 카테고리에 60% 미만일 경우: 카테고리 반환하지 않음
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
케이스 1: 단일 카테고리 (확률 60% 이상, accuracy >= 60)
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

{
    \"accurcy\": 92.25,
    \"categories\": [
        {
            \"code\": \"ROOM\",
            \"name\": \"객실\"
        }
    ]
}

{
    \"accurcy\": 65.34,
    \"categories\": [
        {
            \"code\": \"LOBBY\",
            \"name\": \"로비\"
        }
    ]
}

케이스 2: 복수 카테고리 (최고 확률이 60% 미만, 최고 accuracy < 60.0)
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

{
    \"accurcy\": 53.24,
    \"categories\": [
        {
            \"code\": \"ROOM\",
            \"name\": \"객실\"
        },
        {
            \"code\": \"APPEARANCE\",
            \"name\": \"외관\"
        }
    ]
}

{
    \"accurcy\": 10.91,
    \"categories\": [
        {
            \"code\": \"APPEARANCE\",
            \"name\": \"외관\"
        },
        {
            \"code\": \"VIEW\",
            \"name\": \"전경\"
        }
    ]
}

케이스 3: 모든 카테고리에 해당하는 확률이 60% 미만일 경우
{
    \"accuracy\": 0.0,
    \"message\": \"Unknown\"
}

프로세스 흐름
1. 이미지 수신 및 분석
2. 각 카테고리별 확률 계산
3. 확률에 따른 카테고리 선정
- 최고 확률이 60% 이상: 해당 카테고리만 선정
- 최고 확률이 60% 미만: 상위 2개 카테고리 선정
4. 확률이 60% 미만일 때, 상위 1번째 확률에 대해 accuracy 에 표시
5. 모든 카테고리에 속하지 않을 경우 카테고리 반환하지 않음
6. JSON 형식으로 결과 반환

주의사항
1. 확률 계산은 내부적으로만 사용하며, 결과에는 포함하지 않습니다.
2. 카테고리 이름과 코드는 `3. 카테고리` 에 있는 정보만 활용한다.
3. 응답은 반드시 지정된 JSON 형식을 따라야 합니다.
4. 불확실한 경우 상위 2개 카테고리를 반환하는 것을 선호합니다.
5. 어떤 카테고리에도 속하지 않을 경우 카테고리를 반환하지 않습니다.

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
        
        # Initialize Vertex AI
        vertexai.init(project=project_id, location=location)
        
        # Create generation config
        self.generation_config = {
            "max_output_tokens": 8192,
            "temperature": 0,
            "top_p": 0,
            "response_mime_type": "application/json",
            "response_schema": {
                "type": "OBJECT",
                "properties": {
                    "accuracy": {"type": "NUMBER"},
                    "categories": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "code": {"type": "STRING"},
                                "name": {"type": "STRING"}
                            },
                            "required": ["code", "name"]
                        }
                    }
                },
                "required": ["accuracy", "categories"]
            }
        }
        
        # Set up safety settings
        self.safety_settings = [
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
        
        # Create the model
        self.model = GenerativeModel(
            model_name=model_name,
            system_instruction=[self.system_instruction]
        )
    
    def categorize_image(self, image_path):
        """
        Categorize an image based on the predefined rules.
        
        :param image_path: Path to the image file
        :return: JSON response with categorization results
        """
        try:
            # Open the image file
            image_file = Part.from_uri(image_path, "image/jpeg")
            
            # Generate response
            response = self.model.generate_content(
                [image_file, "이 이미지는 어떤 category 인가?"],
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            # Parse and return the response
            try:
                return json.loads(response.candidates[0].content.parts[0].text)
            except json.JSONDecodeError:
                return {
                    "accuracy": 0.0,
                    "message": "응답 형식 오류"
                }
        
        except FileNotFoundError:
            return {
                "accuracy": 0.0,
                "message": "이미지가 주어지지 않았습니다."
            }
        except Exception as e:
            return {
                "accuracy": 0.0,
                "message": f"분석 중 오류 발생: {str(e)}"
            }
