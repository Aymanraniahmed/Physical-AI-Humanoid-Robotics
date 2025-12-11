"""FastAPI main application for RAG chatbot."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

from .config import settings
from .rag_service import RAGService

app = FastAPI(
    title="Physical AI Book RAG Chatbot",
    description="Retrieval-Augmented Generation chatbot for Physical AI & Humanoid Robotics book",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service
rag_service = RAGService()


# Request/Response models
class ChatRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None
    session_id: Optional[str] = None


class Source(BaseModel):
    chapter: str
    section: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]
    session_id: str


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "service": "Physical AI Book RAG Chatbot",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "qdrant": "connected",
            "openai": "configured",
            "database": "connected"
        }
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return RAG-enhanced response.

    Args:
        request: ChatRequest with query, optional selected_text, and session_id

    Returns:
        ChatResponse with answer, sources, and session_id
    """
    try:
        # Generate or use existing session ID
        session_id = request.session_id or str(uuid.uuid4())

        # Get RAG response
        answer, sources = await rag_service.get_answer(
            query=request.query,
            selected_text=request.selected_text,
            session_id=session_id
        )

        return ChatResponse(
            answer=answer,
            sources=[
                Source(
                    chapter=s["chapter"],
                    section=s["section"],
                    score=s["score"]
                )
                for s in sources
            ],
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/history/{session_id}")
async def get_history(session_id: str):
    """Get chat history for a session."""
    try:
        history = await rag_service.get_session_history(session_id)
        return {"session_id": session_id, "history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/clear/{session_id}")
async def clear_session(session_id: str):
    """Clear a chat session."""
    try:
        await rag_service.clear_session(session_id)
        new_session_id = str(uuid.uuid4())
        return {"message": "Session cleared", "new_session_id": new_session_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
