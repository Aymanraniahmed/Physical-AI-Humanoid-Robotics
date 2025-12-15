"""
Chat aur message ke data models
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ChunkSource(BaseModel):
    """
    Retrieved chunk ki information
    User ko dikhane ke liye ke answer kahan se aaya
    """
    chunk_id: str
    text: str  # Chunk ka text
    score: float  # Similarity score (0-1)
    metadata: Optional[dict] = None  # Page number, chapter, etc.


class ChatRequest(BaseModel):
    """
    Normal RAG chat request
    User ka sawal aur book_id (optional - default book use hogi)
    """
    book_id: Optional[str] = "default"  # Default book auto-loaded hai
    message: str
    session_id: Optional[str] = None  # Multi-turn conversation ke liye


class ChatResponse(BaseModel):
    """
    Chat API response
    Answer aur sources (proof) ke saath
    """
    session_id: str
    response: str  # AI ka jawab
    sources: List[ChunkSource]  # Kahan se answer aaya


class SelectionChatRequest(BaseModel):
    """
    Selected text Q&A request
    User ne text highlight kiya aur sawal poocha
    """
    selected_text: str
    question: str
    session_id: Optional[str] = None


class SelectionChatResponse(BaseModel):
    """
    Selection chat response
    Sirf answer, sources nahi (kyunki Qdrant use nahi hua)
    """
    session_id: str
    response: str


class ErrorResponse(BaseModel):
    """
    Error response model
    """
    error: str
    detail: Optional[str] = None
    request_id: Optional[str] = None
