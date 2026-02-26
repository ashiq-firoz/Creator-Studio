import boto3
from boto3.dynamodb.conditions import Key, Attr
from typing import Optional, Dict, Any, List
from datetime import datetime
from .config import settings
import uuid


class DynamoDBClient:
    def __init__(self):
        if settings.use_localstack and settings.localstack_endpoint:
            self.dynamodb = boto3.resource(
                'dynamodb',
                endpoint_url=settings.localstack_endpoint,
                region_name=settings.aws_region,
                aws_access_key_id='test',
                aws_secret_access_key='test'
            )
        else:
            self.dynamodb = boto3.resource(
                'dynamodb',
                region_name=settings.aws_region
            )
        
        self.tables = {
            'users': f"{settings.dynamodb_table_prefix}-users",
            'content': f"{settings.dynamodb_table_prefix}-content",
            'adaptations': f"{settings.dynamodb_table_prefix}-adaptations",
            'publish_jobs': f"{settings.dynamodb_table_prefix}-publish-jobs",
            'analytics': f"{settings.dynamodb_table_prefix}-analytics",
            'ad_placements': f"{settings.dynamodb_table_prefix}-ad-placements"
        }
    
    def create_tables(self):
        """Create all required DynamoDB tables"""
        try:
            # Users table
            self.dynamodb.create_table(
                TableName=self.tables['users'],
                KeySchema=[
                    {'AttributeName': 'id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'},
                    {'AttributeName': 'email', 'AttributeType': 'S'}
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'email-index',
                        'KeySchema': [{'AttributeName': 'email', 'KeyType': 'HASH'}],
                        'Projection': {'ProjectionType': 'ALL'},
                        'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                    }
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            
            # Content table
            self.dynamodb.create_table(
                TableName=self.tables['content'],
                KeySchema=[
                    {'AttributeName': 'id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'},
                    {'AttributeName': 'user_id', 'AttributeType': 'S'}
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'user-index',
                        'KeySchema': [{'AttributeName': 'user_id', 'KeyType': 'HASH'}],
                        'Projection': {'ProjectionType': 'ALL'},
                        'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                    }
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            
            # Adaptations table
            self.dynamodb.create_table(
                TableName=self.tables['adaptations'],
                KeySchema=[
                    {'AttributeName': 'id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'},
                    {'AttributeName': 'content_id', 'AttributeType': 'S'}
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'content-index',
                        'KeySchema': [{'AttributeName': 'content_id', 'KeyType': 'HASH'}],
                        'Projection': {'ProjectionType': 'ALL'},
                        'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                    }
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            
            # Publish jobs table
            self.dynamodb.create_table(
                TableName=self.tables['publish_jobs'],
                KeySchema=[
                    {'AttributeName': 'id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'},
                    {'AttributeName': 'content_id', 'AttributeType': 'S'}
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'content-index',
                        'KeySchema': [{'AttributeName': 'content_id', 'KeyType': 'HASH'}],
                        'Projection': {'ProjectionType': 'ALL'},
                        'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                    }
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            
            # Analytics table
            self.dynamodb.create_table(
                TableName=self.tables['analytics'],
                KeySchema=[
                    {'AttributeName': 'id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'},
                    {'AttributeName': 'content_id', 'AttributeType': 'S'}
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'content-index',
                        'KeySchema': [{'AttributeName': 'content_id', 'KeyType': 'HASH'}],
                        'Projection': {'ProjectionType': 'ALL'},
                        'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                    }
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            
            # Ad placements table
            self.dynamodb.create_table(
                TableName=self.tables['ad_placements'],
                KeySchema=[
                    {'AttributeName': 'id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'},
                    {'AttributeName': 'content_id', 'AttributeType': 'S'}
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'content-index',
                        'KeySchema': [{'AttributeName': 'content_id', 'KeyType': 'HASH'}],
                        'Projection': {'ProjectionType': 'ALL'},
                        'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
                    }
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            
            print("All tables created successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")
    
    def get_table(self, table_name: str):
        return self.dynamodb.Table(self.tables[table_name])
    
    # User operations
    def create_user(self, user_data: Dict[str, Any]) -> str:
        user_id = str(uuid.uuid4())
        user_data['id'] = user_id
        user_data['created_at'] = datetime.utcnow().isoformat()
        
        table = self.get_table('users')
        table.put_item(Item=user_data)
        return user_id
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        table = self.get_table('users')
        response = table.get_item(Key={'id': user_id})
        return response.get('Item')
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        table = self.get_table('users')
        response = table.query(
            IndexName='email-index',
            KeyConditionExpression=Key('email').eq(email)
        )
        items = response.get('Items', [])
        return items[0] if items else None
    
    # Content operations
    def create_content(self, content_data: Dict[str, Any]) -> str:
        content_id = str(uuid.uuid4())
        content_data['id'] = content_id
        content_data['created_at'] = datetime.utcnow().isoformat()
        
        table = self.get_table('content')
        table.put_item(Item=content_data)
        return content_id
    
    def get_content(self, content_id: str) -> Optional[Dict[str, Any]]:
        table = self.get_table('content')
        response = table.get_item(Key={'id': content_id})
        return response.get('Item')
    
    def update_content(self, content_id: str, updates: Dict[str, Any]):
        table = self.get_table('content')
        update_expression = "SET " + ", ".join([f"#{k} = :{k}" for k in updates.keys()])
        expression_attribute_names = {f"#{k}": k for k in updates.keys()}
        expression_attribute_values = {f":{k}": v for k, v in updates.items()}
        
        table.update_item(
            Key={'id': content_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )
    
    def get_user_content(self, user_id: str) -> List[Dict[str, Any]]:
        table = self.get_table('content')
        response = table.query(
            IndexName='user-index',
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        return response.get('Items', [])
    
    # Adaptation operations
    def create_adaptation(self, adaptation_data: Dict[str, Any]) -> str:
        adaptation_id = str(uuid.uuid4())
        adaptation_data['id'] = adaptation_id
        adaptation_data['created_at'] = datetime.utcnow().isoformat()
        
        table = self.get_table('adaptations')
        table.put_item(Item=adaptation_data)
        return adaptation_id
    
    def get_content_adaptations(self, content_id: str) -> List[Dict[str, Any]]:
        table = self.get_table('adaptations')
        response = table.query(
            IndexName='content-index',
            KeyConditionExpression=Key('content_id').eq(content_id)
        )
        return response.get('Items', [])
    
    # Publish job operations
    def create_publish_job(self, job_data: Dict[str, Any]) -> str:
        job_id = str(uuid.uuid4())
        job_data['id'] = job_id
        job_data['created_at'] = datetime.utcnow().isoformat()
        
        table = self.get_table('publish_jobs')
        table.put_item(Item=job_data)
        return job_id
    
    def get_publish_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        table = self.get_table('publish_jobs')
        response = table.get_item(Key={'id': job_id})
        return response.get('Item')
    
    def update_publish_job(self, job_id: str, updates: Dict[str, Any]):
        table = self.get_table('publish_jobs')
        update_expression = "SET " + ", ".join([f"#{k} = :{k}" for k in updates.keys()])
        expression_attribute_names = {f"#{k}": k for k in updates.keys()}
        expression_attribute_values = {f":{k}": v for k, v in updates.items()}
        
        table.update_item(
            Key={'id': job_id},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values
        )


# Global database client instance
db = DynamoDBClient()
