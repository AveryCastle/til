import boto3
from boto3.dynamodb.conditions import Key, Attr  # Key와 Attr import 추가
import uuid

class DatabaseAccess():
    def __init__(self, TABLE_NAME):
        # DynamoDB 세팅
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(TABLE_NAME)

    def get_data(self, input_key):
        res = self.table.get_item(Key=input_key)
        if 'Item' in res:
            item = res['Item']
            print(f"found data={item}")
            return item
        else:
            None
    
    def query_events_by_attribute(self, key_name, key_value, attribute_name, attribute_value):
        
        # Query 실행
        response = self.table.query(
            KeyConditionExpression=Key(key_name).eq(key_value),
            FilterExpression=Attr(attribute_name).eq(attribute_value)
        )
        
        # 결과 추출
        items = response.get('Items', [])
        return items

    
    def put_data(self, input_data):
        self.table.put_item(Item =  input_data)
        print(f"Putting data '{input_data}' is completed!")

    def delete_data(self, input_key):
        self.table.delete_item(
            Key = input_key
        )

def generate_conversation_id_with_uuid(user_id):
    return f"conv-{user_id}-{uuid.uuid4()}"
