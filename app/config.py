"""Configuration management"""
import os
from typing import Optional


class Config:
    """Application configuration"""

    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    # Google
    GOOGLE_API_KEY: Optional[str] = os.getenv("GOOGLE_API_KEY")

    # Cache
    CACHE_TTL: int = int(os.getenv("CACHE_TTL", "300"))

    # Pipeline
    PIPELINE_TIMEOUT: int = int(os.getenv("PIPELINE_TIMEOUT", "30"))

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


config = Config()
