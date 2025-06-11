"""
Configuration management for the URL shortener backend.
"""
import os
from typing import Optional


class Settings:
    """Application settings with environment variable support."""
    
    # Database settings
    database_url: str = "sqlite:///./data/url_shortener.db"
    database_echo: bool = False
    
    # API settings
    api_title: str = "URL Shortener API"
    api_version: str = "1.0.0"
    api_description: str = "A simple URL shortener service"
    
    # CORS settings
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:3001"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]
    
    # Security settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application settings
    short_code_length: int = 6
    base_url: str = "http://localhost:8000"
    
    # Logging settings
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_format: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    def __init__(self):
        """Initialize settings with environment variables."""
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./data/url_shortener.db")
        self.database_echo = os.getenv("DATABASE_ECHO", "False").lower() == "true"
        
        self.api_title = os.getenv("API_TITLE", "URL Shortener API")
        self.api_version = os.getenv("API_VERSION", "1.0.0")
        self.api_description = os.getenv("API_DESCRIPTION", "A simple URL shortener service")
        
        self.cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")
        self.cors_allow_credentials = os.getenv("CORS_ALLOW_CREDENTIALS", "True").lower() == "true"
        self.cors_allow_methods = ["*"]
        self.cors_allow_headers = ["*"]
        
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        
        self.short_code_length = int(os.getenv("SHORT_CODE_LENGTH", "6"))
        self.base_url = os.getenv("BASE_URL", "http://localhost:8000")
        
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_format = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")


# Global settings instance
settings = Settings() 