"""
Chat API endpoints
POST /chat - Normal RAG chat
POST /chat/selection - Selected text Q&A
"""

from fastapi import APIRouter, HTTPException
from app.models.chat import (
    ChatRequest,
    ChatResponse,
    SelectionChatRequest,
    SelectionChatResponse,
    ErrorResponse
)
from app.services.chat_service import chat_service, selection_chat_service


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Normal RAG chatbot
    User ka sawal -> Book se relevant chunks dhundo -> Answer generate karo

    Request:
    - book_id: Kis book se answer chahiye
    - message: User ka sawal
    - session_id: Optional - conversation continue karne ke liye

    Response:
    - session_id: Conversation ID
    - response: AI ka jawab
    - sources: Kahan se answer aaya (chunks with scores)
    """

    try:
        # Chat service call karo
        result = chat_service.chat(
            book_id=request.book_id,
            user_message=request.message,
            session_id=request.session_id
        )

        return ChatResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}"
        )


@router.post("/selection", response_model=SelectionChatResponse)
async def chat_selection(request: SelectionChatRequest):
    """
    Selected text Q&A
    User ne text highlight kiya aur sawal poocha

    IMPORTANT: Ye Qdrant use NAHI karta - sirf selected text se answer deta hai

    Request:
    - selected_text: User ne jo text highlight kiya
    - question: User ka sawal
    - session_id: Optional

    Response:
    - session_id: Conversation ID
    - response: AI ka jawab (sirf selected text ke basis par)
    """

    # Text length validate karo
    if len(request.selected_text) > 10000:
        raise HTTPException(
            status_code=400,
            detail="Selected text is too long. Maximum 10000 characters allowed."
        )

    try:
        # Selection chat service call karo
        result = selection_chat_service.chat_selection(
            selected_text=request.selected_text,
            question=request.question,
            session_id=request.session_id
        )

        return SelectionChatResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}"
        )
