"""Application Configuration"""

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = "postgresql://isp_user:isp_password@db:5432/isp_os"
    
    # Redis
    redis_url: str = "redis://redis:6379/0"
    
    # FastAPI
    fastapi_env: str = "development"
    fastapi_debug: bool = True
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    jwt_secret_key: str = "your-jwt-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://frontend:3000",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
