"""
Configuration settings for RAG Chatbot
Yahan saari settings aur environment variables load hoti hain
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """
    Application settings
    .env file se automatically load ho jayengi
    """

    # Google Gemini Settings (OpenAI ki jagah)
    gemini_api_key: str
    embedding_model: str = "all-MiniLM-L6-v2"  # Local sentence-transformers model
    chat_model: str = "models/gemini-2.5-flash"  # Gemini chat model (fast & efficient)

    # Qdrant Settings
    qdrant_url: str = ":memory:"  # In-memory mode (no Docker needed)
    qdrant_api_key: str = ""  # Optional for local
    qdrant_collection_name: str = "book_chunks"
    embedding_dimension: int = 384  # all-MiniLM-L6-v2 model dimension

    # Chunking Settings
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Database Settings (optional)
    database_url: str = "postgresql://raguser:ragpassword@localhost:5432/ragchatbot"

    # App Settings
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True

    # CORS Settings
    allowed_origins: str = "http://localhost:3000,http://localhost:8000,http://127.0.0.1:3000,http://127.0.0.1:8000"

    class Config:
        # .env file ka naam
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def origins_list(self) -> List[str]:
        """CORS origins ko list mein convert karta hai"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


# Global settings object
# Isko import karke use karo: from app.config import settings
settings = Settings()
