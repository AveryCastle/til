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
DB_HOST = 'with-yeogi-rds-read.abouthere.kr' #os.environ['DB_HOST']
DB_NAME = 'yeogi' #os.environ['DB_NAME']
DB_USER = 'yeogi' #'within_dev' #'yeogi' #os.environ['DB_USER']
DB_PASSWORD = 'DQlapaTm&79()' #'With!n@()' #'DQlapaTm&79()' #os.environ['DB_PASSWORD']
SQS_QUEUE_URL = 'https://sqs.ap-northeast-2.amazonaws.com/269388641688/d-stay-exhibition-property-image-processing-queue' #os.environ['SQS_QUEUE_URL']

# Initialize AWS clients
sqs = boto3.client('sqs')

def get_db_connection():
    """Create and return a database connection"""
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            passwd=DB_PASSWORD,
            db=DB_NAME,
            connect_timeout=5,
            cursorclass=pymysql.cursors.DictCursor,
            port=3306
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
                WHERE pi.property_seq = %s
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

def send_to_sqs(messages):
    """Send messages to SQS queue in batches"""
    batch_size = 10  # SQS allows maximum 10 messages per batch
    
    for i in range(0, len(messages), batch_size):
        batch = messages[i:i + batch_size]
        
        entries = [
            {
                'Id': str(idx),
                'MessageBody': json.dumps(msg),
                'MessageAttributes': {
                    'PropertySeq': {
                        'DataType': 'Number',
                        'StringValue': str(msg['property_seq'])
                    }
                }
            }
            for idx, msg in enumerate(batch)
        ]
        
        try:
            response = sqs.send_message_batch(
                QueueUrl=SQS_QUEUE_URL,
                Entries=entries
            )
            
            # Log successful and failed messages
            if 'Successful' in response:
                logger.info(f"Successfully sent {len(response['Successful'])} messages to SQS")
            if 'Failed' in response:
                logger.error(f"Failed to send {len(response['Failed'])} messages to SQS: {response['Failed']}")
                
        except ClientError as e:
            logger.error(f"Error sending messages to SQS: {str(e)}")
            raise

def lambda_handler(event, context):
    """Main Lambda handler"""
    try:
        # Extract property_seq from the event
        if 'property_seq' not in event:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'property_seq is required'})
            }
        
        property_seq = 0
        for property_seq in event['property_seq']:
            property_seq = int(property_seq)
            logger.info(f"Processing property_seq: {property_seq}")
            
            # Get images from database
            images = get_property_images(property_seq)
            if not images:
                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': f'No images found for property_seq: {property_seq}'})
                }
                
            logger.info(f"Found {len(images)} images for property_seq: {property_seq}")
            
            # Prepare messages for SQS
            messages = [
                {
                    'property_seq': img['property_seq'],
                    'property_image_seq': img['property_image_seq'],
                    'image_seq': img['image_seq'],
                    'image_path': img['image_path']
                }
                for img in images
            ]
            
            # Send messages to SQS
            send_to_sqs(messages)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Successfully processed {len(images)} images for property_seq: {property_seq}',
                'image_count': len(images)
            })
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }