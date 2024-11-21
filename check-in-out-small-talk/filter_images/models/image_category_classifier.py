import logging
import json
import time
from typing import List
from models.vertex_image_categorizer import VertexImageCategorizer
from models.database_manager import DatabaseManager

class ImageCategoryClassifier:
    def __init__(self, image_categorizer: VertexImageCategorizer):
        """
        Initialize the image category classifier.
        
        Args:
            image_categorizer: Vertex AI generative model
            generation_config: Generation configuration for model
            safety_settings: Safety settings for model queries
        """
        self.image_categorizer = image_categorizer
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
            response = self.image_categorizer.categorize_image(image_path)
            return response
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
                    image_category = self.classify_image_category(property_image['image_path'])
                    if image_category.get('message') == 'Unknown':
                        time.sleep(10)
                        self.logger.info("Woke up after 10 seconds.")

                    if len(image_category.get('categories', [])) > 0:
                        self.logger.info(f"Selected property {property_image['property_seq']}, image {property_image['property_image_seq']}'s accuracy is {image_category.get('accuracy')}")
                        db_manager.update_image(
                            property_seq = property_image['property_seq'],
                            image_seq = property_image['property_image_seq'], 
                            image_accuracy = image_category.get('accuracy'), 
                            image_category = image_category.get('categories')[0]['code']
                        )
                    else:
                        self.logger.warning(f"property {property_image['property_seq']}'s image {property_image['property_image_seq']}: no categories found in image classification response.")
                self.logger.info(f"Processed images for property {property_id}")
            
            except Exception as e:
                self.logger.error(f"Error processing property {property_id}: {e}")

