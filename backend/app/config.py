"""Configuration settings for the RAG chatbot backend."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI Configuration
    openai_api_key: str
    embedding_model: str = "text-embedding-3-small"
    chat_model: str = "gpt-4-turbo-preview"

    # Qdrant Configuration
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection: str = "book_chunks"

    # Database Configuration
    database_url: str

    # RAG Configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_results: int = 5

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list = ["http://localhost:3000", "https://*.vercel.app"]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
