"""
Health check endpoint
GET /health - System health check
"""

from fastapi import APIRouter
from app.services.vector_store import vector_store
from app.config import settings


router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """
    System health check
    Saari services (Qdrant, Local Embeddings) working hain ya nahi check karo

    Returns:
    - status: "healthy" ya "degraded"
    - services: Har service ka status
    """

    health_status = {
        "status": "healthy",
        "services": {},
        "message": "RAG Chatbot with Local Embeddings"
    }

    # Qdrant check karo
    try:
        qdrant_healthy = vector_store.health_check()
        health_status["services"]["qdrant"] = "up" if qdrant_healthy else "down"
    except Exception as e:
        health_status["services"]["qdrant"] = f"down: {str(e)}"
        health_status["status"] = "degraded"

    # Local Embeddings always available (no API needed)
    health_status["services"]["embeddings"] = "up (local model)"

    # Gemini optional for chat
    health_status["services"]["chat_model"] = f"{settings.chat_model} (Gemini)"

    return health_status
