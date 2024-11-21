import logging
from models.database_manager import DatabaseManager
from models.image_category_classifier import ImageCategoryClassifier
from models.vertex_image_categorizer import VertexImageCategorizer

def main():
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Vertex AI 초기화
    ai_image_categorizer = VertexImageCategorizer(project_id='seb-dev-440401')

    # 데이터베이스 관리자 초기화
    db_manager = DatabaseManager()
    
    # 예제 속성 ID
    property_ids = [6674]  # 필요에 따라 ID 추가
    
    # 분류기 초기화
    classifier = ImageCategoryClassifier(image_categorizer=ai_image_categorizer)
    
    # 이미지 카테고리 처리
    classifier.update_image_categories(property_ids, db_manager)

if __name__ == '__main__':
    main()