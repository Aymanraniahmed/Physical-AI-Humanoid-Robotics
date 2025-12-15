"""
Book aur chunk ke data models
Pydantic use karke data validation hoti hai
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class BookMetadata(BaseModel):
    """Book ki extra information"""
    author: Optional[str] = None
    title: Optional[str] = None
    page_count: Optional[int] = None
    file_type: Optional[str] = None  # pdf, html, epub


class ChunkMetadata(BaseModel):
    """Chunk ki extra information"""
    page_number: Optional[int] = None
    chapter: Optional[str] = None
    section: Optional[str] = None


class BookChunk(BaseModel):
    """
    Book ka ek chunk (tukda)
    Har chunk text-embedding-3-small se embed hoga
    """
    chunk_id: str
    book_id: str
    chunk_index: int  # Kaunsa number ka chunk hai (0, 1, 2...)
    text: str  # Chunk ka text content
    metadata: Optional[ChunkMetadata] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Book(BaseModel):
    """
    Book ki complete information
    """
    book_id: str
    title: str
    total_chunks: int
    metadata: Optional[BookMetadata] = None
    ingested_at: datetime = Field(default_factory=datetime.utcnow)


class IngestRequest(BaseModel):
    """
    Book upload request
    Frontend se file upload hogi toh ye data aayega
    """
    book_id: Optional[str] = None  # Agar nahi diya toh auto-generate hoga
    metadata: Optional[Dict[str, Any]] = None


class IngestResponse(BaseModel):
    """
    Upload ke baad jo response jayega
    """
    book_id: str
    title: str
    total_chunks: int
    status: str  # "completed" ya "failed"
    message: Optional[str] = None
