from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # AWS Configuration
    aws_region: str = "us-east-1"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    s3_bucket_name: str = "creator-dashboard-videos"
    dynamodb_table_prefix: str = "creator-dashboard"
    
    # Bedrock Models
    bedrock_model_text: str = "us.amazon.nova-lite-v1:0"
    bedrock_model_vision: str = "us.amazon.nova-pro-v1:0"
    
    # Security
    jwt_secret: str = "change-this-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # LocalStack (for development)
    use_localstack: bool = False
    localstack_endpoint: Optional[str] = None
    
    # Social Media APIs
    youtube_client_id: Optional[str] = None
    youtube_client_secret: Optional[str] = None
    instagram_app_id: Optional[str] = None
    instagram_app_secret: Optional[str] = None
    tiktok_client_key: Optional[str] = None
    tiktok_client_secret: Optional[str] = None
    twitter_api_key: Optional[str] = None
    twitter_api_secret: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
