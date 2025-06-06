from pydantic_settings import BaseSettings
from typing import Optional
import secrets
from functools import lru_cache

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Pharmacy Management System"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # AWS Settings
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    
    # DynamoDB Settings
    DYNAMODB_TABLE_PREFIX: str = "pms_"
    
    # Redis Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    
    # Database Settings
    # To override the database URL, create a .env file in the backend directory with:
    # DATABASE_URL=postgresql://username:password@localhost:5432/pms
    # or your actual database connection string
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/pms"
    
    # ML Model Settings
    MODEL_PATH: str = "app/ml/models"
    BATCH_SIZE: int = 32
    
    # File Upload Settings
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE: int = 5 * 1024 * 1024  # 5MB
    
    class Config:
        case_sensitive = True
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 