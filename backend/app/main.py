"""
FastAPI Main Application
RAG Chatbot Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import health, ingest, chat
from app.startup import auto_load_book


# FastAPI app initialize karo
app = FastAPI(
    title="RAG Chatbot API",
    description="Retrieval-Augmented Generation chatbot for Physical AI Humanoid Robotics book",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI: http://localhost:8000/docs
    redoc_url="/redoc"  # ReDoc: http://localhost:8000/redoc
)


# CORS middleware add karo
# Frontend se API calls allowed hongi
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, etc. sab allowed
    allow_headers=["*"],  # All headers allowed
)


# Routers include karo
app.include_router(health.router)
app.include_router(ingest.router)
app.include_router(chat.router)


# Root endpoint
@app.get("/")
async def root():
    """
    API root endpoint
    """
    return {
        "message": "RAG Chatbot API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    App start hone par ye run hoga
    Book automatically load ho jayegi - user ko upload nahi karna padega
    """
    print("\n" + "="*60)
    print("RAG Chatbot API Starting...")
    print("="*60)
    print(f"Chat Model: {settings.chat_model}")
    print(f"Embedding Model: {settings.embedding_model} (Local)")
    print(f"Qdrant URL: {settings.qdrant_url}")
    print(f"Docs: http://{settings.app_host}:{settings.app_port}/docs")
    print("="*60 + "\n")

    # Auto-load book on startup
    auto_load_book()


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    App shutdown hone par cleanup
    """
    print("\nShutting down RAG Chatbot API...")


if __name__ == "__main__":
    import uvicorn

    # Server run karo
    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.debug  # Auto-reload in development mode
    )
