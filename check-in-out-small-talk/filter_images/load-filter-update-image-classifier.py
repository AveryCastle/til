import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part
import json
import os
import logging
import pymysql
import boto3
from botocore.exceptions import ClientError
from contextlib import contextmanager
from typing import Optional, Union, List, Tuple, Dict
import time

vertexai.init(project="seb-dev-440401", location="asia-northeast3")

textsi_1 = """
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

model = GenerativeModel(
    model_name="gemini-1.5-pro-002",
    system_instruction=[textsi_1]
)

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

# Environment variables
DB_HOST = 'with-yeogi-rds-read.abouthere.kr'#os.environ['DB_HOST']
DB_NAME = 'yeogi' # os.environ['DB_NAME']
DB_USER = 'within_dev'# 'within_dev' # 'yeogi' #os.environ['DB_USER']
DB_PASSWORD = 'With!n@()' #'With!n@()' # 'DQlapaTm&79()' #os.environ['DB_PASSWORD']

class DatabaseManager:
    def __init__(self, 
                 host='localhost', 
                 database='your_database', 
                 user='your_username', 
                 password='your_password', 
                 port=3306):
        """
        Initialize database connection parameters.
        
        Args:
            host (str): Database host
            database (str): Database name
            user (str): Database username
            password (str): Database password
            port (int): Database port
        """
        self.config = {
            'host': host,
            'database': database,
            'user': user,
            'password': password,
            'port': port,
            'charset': 'utf8mb4',
            'connect_timeout': 5,
            'read_timeout': 60,
            'write_timeout': 60,
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.logger = logging.getLogger(__name__)

    @contextmanager
    def get_connection(self):
        """
        Context manager to get database connection.
        
        Yields:
            pymysql connection object
        """
        connection = None
        try:
            connection = pymysql.connect(**self.config)
            yield connection
        except pymysql.Error as error:
            self.logger.error(f"Database connection error: {error}")
            raise
        finally:
            if connection:
                connection.close()

    def get_all_property_images(self) -> List[Dict[str, Union[int, str]]]:
        """
        Retrieve property images for a given property sequence.
        
        Args:
            property_seq (int): Property sequence number
        
        Returns:
            List of dictionaries containing image details
        """
        query = """
        SELECT
                pi.property_seq,
                pi.property_image_seq,
                pi.image_seq,
                CONCAT('https://dev-image.withinapi.com', '', ti.path, '/', ti.file_name, '.', ti.mime_type) as image_path
         FROM tb_property_image pi
   INNER JOIN tb_image ti ON pi.image_seq = ti.image_seq
        WHERE 1=1
          AND pi.image_type = 'HOTEL_AFFILIATE'
          AND pi.property_image_category IS NULL
     ORDER BY pi.image_sort
        """
        
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    connection.commit()
            return results
        except Exception as e:
            self.logger.error(f"Error retrieving property images for property {property_seq}: {e}")
            return []

    def get_property_images(self, property_seq: int) -> List[Dict[str, Union[int, str]]]:
        """
        Retrieve property images for a given property sequence.
        
        Args:
            property_seq (int): Property sequence number
        
        Returns:
            List of dictionaries containing image details
        """
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
        
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (property_seq,))
                    results = cursor.fetchall()
                    connection.commit()
            return results
        except Exception as e:
            self.logger.error(f"Error retrieving property images for property {property_seq}: {e}")
            return []
        
    def update_image(self, image_seq: int, image_category: str) -> int:
        """
        Update image category for a specific image sequence.
        
        Args:
            image_seq (int): Image sequence number
            image_category (str): Category to update
        
        Returns:
            int: Number of rows affected
        """
        # Update my_image table with image category
        query = """
        UPDATE tb_property_image 
           SET property_image_category = %s 
         WHERE property_image_seq = %s
        """
        
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (image_category, image_seq))
                    rows_affected = cursor.rowcount
                    connection.commit()
            
            self.logger.info(f"Updated image {image_seq} with category {image_category}")
            return rows_affected
        except Exception as e:
            self.logger.error(f"Error updating image {image_seq}: {e}")
            return 0


class ImageCategoryClassifier:
    def __init__(self, model, generation_config, safety_settings):
        """
        Initialize the image category classifier.
        
        Args:
            model: Vertex AI generative model
            generation_config: Generation configuration for model
            safety_settings: Safety settings for model queries
        """
        self.model = model
        self.generation_config = generation_config
        self.safety_settings = safety_settings
        self.logger = logging.getLogger(__name__)

    def classify_image_category(self, image_path: str) -> str:
        """
        Classify the category of an image using Vertex AI.
        
        Args:
            image_path (str): Path to the image file
        
        Returns:
            str: Identified image category
        """
        try:
            image_file = Part.from_uri(image_path, "image/jpeg")
            response = self.model.generate_content(
                [image_file, "이 이미지는 어떤 category 인가?"],
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            return response.candidates[0].content.parts[0].text
        except Exception as e:
            self.logger.error(f"Error classifying image {image_path}: {e}")
            return "{ \"accuracy\": 0.0, \"message\": \"Unknown\" }"

    def update_image_categories(self, property_ids: List[int], db_manager: DatabaseManager) -> None:
        """
        Update image categories for given property IDs.
        
        Args:
            property_ids (List[int]): List of property IDs to process
            db_manager (DatabaseManager): Database manager for query execution
        """
        for property_id in property_ids:
            try:
                property_images = db_manager.get_all_property_images()
                
                for property_image in property_images:
                    image_category_result = self.classify_image_category(property_image['image_path'])
                    image_category = json.loads(image_category_result)
                    if image_category.get('message') == 'Unknown':
                        time.sleep(10)
                        self.logger.info("Woke up after 10 seconds.")

                    if len(image_category.get('categories', [])) > 0:
                        self.logger.info(f"Selected property {property_image['property_seq']}, image {property_image['property_image_seq']}'s accuracy is {image_category.get('accuracy')}")
                        db_manager.update_image(property_image['property_image_seq'], image_category.get('categories')[0]['code'])
                    else:
                        self.logger.warning(f"property {property_image['property_seq']}'s image {property_image['property_image_seq']}: no categories found in image classification response.")
                self.logger.info(f"Processed images for property {property_id}")
            
            except Exception as e:
                self.logger.error(f"Error processing property {property_id}: {e}")


def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Example property IDs
    property_ids = [6674] #[76065, 6674]  # Add more IDs as needed
    
    # Initialize classifier with existing model, configs
    classifier = ImageCategoryClassifier(
        model=model, 
        generation_config=generation_config, 
        safety_settings=safety_settings
    )

    # Global database manager instance
    db_manager = DatabaseManager(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    # Process image categories
    classifier.update_image_categories(property_ids, db_manager)


if __name__ == '__main__':
    main()
