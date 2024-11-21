import pymysql
import logging
from contextlib import contextmanager
from typing import List, Dict, Union
from config.database_config import DB_CONFIG

class DatabaseManager:
    def __init__(self, config=DB_CONFIG):
        """
        Initialize database connection parameters.
        """
        self.config = {
            **config,
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
                i.ano AS property_seq,
                i.property_image_seq,
                i.image_seq,
                i.image_path
         FROM image_hackathon i
        WHERE 1=1
          AND i.image_type = 'HOTEL_AFFILIATE'
          AND i.property_image_category IS NULL
     ORDER BY i.ano, i.image_sort
        """
        
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    connection.commit()
            return results
        except Exception as e:
            self.logger.error(f"Error retrieving property images for property: {e}")
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
                i.ano as property_seq,
                i.property_image_seq,
                i.image_seq,
                i.image_path
         FROM image_hackathon i
        WHERE 1=1
          AND i.image_type = 'HOTEL_AFFILIATE'
          AND i.ano = %s
          AND i.property_image_category IS NULL
     ORDER BY i.image_sort
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
        
    def update_image(self, property_seq: int, image_seq: int, image_accuracy: float, image_category: str) -> int:
        """
        Update image category for a specific image sequence.
        
        Args:
            property_seq (int): Property sequence number
            image_seq (int): Image sequence number
            image_accuracy (float): Image Accuracy to update
            image_category (str): Category to update
        
        Returns:
            int: Number of rows affected
        """
        # Update my_image table with image category
        query = """
        UPDATE image_hackathon 
           SET property_image_category = %s,
               property_image_accuracy = %s
         WHERE ano = %s
           AND property_image_seq = %s
        """
        
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (image_category, image_accuracy, property_seq, image_seq))
                    rows_affected = cursor.rowcount
                    connection.commit()
            
            self.logger.info(f"Updated image {image_seq} with category {image_category}")
            return rows_affected
        except Exception as e:
            self.logger.error(f"Error updating image {image_seq}: {e}")
            return 0
