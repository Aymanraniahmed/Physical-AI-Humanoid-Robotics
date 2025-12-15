"""
RAG Chat Service
Retrieval-Augmented Generation ke liye main service
Google Gemini use karta hai
"""

import google.generativeai as genai
from typing import List, Dict, Any
from app.config import settings
from app.services.embedding import embedding_service
from app.services.vector_store import vector_store
from app.models.chat import ChunkSource
import uuid


class ChatService:
    """
    Normal RAG chat service
    Query -> Embed -> Search -> Generate Answer
    """

    def __init__(self):
        """Initialize Gemini client"""
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.chat_model)

    def chat(
        self,
        book_id: str,
        user_message: str,
        session_id: str = None
    ) -> Dict[str, Any]:
        """
        RAG chatbot ka main function

        Flow:
        1. User query ko embed karo
        2. Qdrant mein similar chunks search karo
        3. Retrieved chunks ko context bana kar LLM ko do
        4. LLM se answer generate karo

        Args:
            book_id: Kis book se answer nikalna hai
            user_message: User ka sawal
            session_id: Conversation ID (optional)

        Returns:
            Dict with response and sources
        """

        # Step 1: User query ko embedding mein convert karo
        print(f"Embedding user query: {user_message[:50]}...")
        query_embedding = embedding_service.generate_embedding(user_message)

        # Step 2: Qdrant se similar chunks retrieve karo
        print(f"Searching in Qdrant for book_id: {book_id}")
        search_results = vector_store.search(
            query_embedding=query_embedding,
            book_id=book_id,
            limit=5  # Top 5 most relevant chunks
        )

        if not search_results:
            return {
                "session_id": session_id or str(uuid.uuid4()),
                "response": "Sorry, I couldn't find relevant information in the book to answer your question.",
                "sources": []
            }

        # Step 3: Retrieved chunks se context banao
        context_text = "\n\n".join([
            f"[Chunk {i+1}]:\n{chunk['text']}"
            for i, chunk in enumerate(search_results)
        ])

        # Step 4: Prompt build karo
        prompt = f"""You are a helpful AI assistant for a Physical AI and Humanoid Robotics book.
Your job is to answer questions ONLY based on the provided book content.

Rules:
1. Answer only from the provided context
2. If the answer is not in the context, say "This information is not available in the book."
3. Be accurate and cite specific information from the chunks
4. Keep answers clear and concise

Book Context:
{context_text}

Question: {user_message}

Answer:"""

        # Step 5: Gemini se answer generate karo
        print("Generating answer from Gemini...")
        try:
            response = self.model.generate_content(prompt)
            answer = response.text

        except Exception as e:
            print(f"Error generating answer: {e}")
            raise

        # Step 6: Sources format karo (user ko proof dikhane ke liye)
        sources = [
            ChunkSource(
                chunk_id=chunk["chunk_id"],
                text=chunk["text"][:200] + "...",  # First 200 chars
                score=chunk["score"],
                metadata=chunk["metadata"]
            )
            for chunk in search_results
        ]

        # Final response
        return {
            "session_id": session_id or str(uuid.uuid4()),
            "response": answer,
            "sources": sources
        }


class SelectionChatService:
    """
    Selected text Q&A service
    Isme Qdrant use NAHI hoga, sirf selected text par answer
    """

    def __init__(self):
        """Initialize Gemini client"""
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.chat_model)

    def chat_selection(
        self,
        selected_text: str,
        question: str,
        session_id: str = None
    ) -> Dict[str, Any]:
        """
        Selected text ke basis par answer do
        NO QDRANT - sirf text aur question

        Args:
            selected_text: User ne jo text highlight kiya
            question: User ka sawal
            session_id: Conversation ID (optional)

        Returns:
            Dict with response
        """

        # Prompt build karo
        prompt = f"""You are a helpful AI assistant.
Answer the user's question based ONLY on the provided selected text.

Rules:
1. Answer only from the selected text
2. If the answer is not in the selected text, say "I cannot answer this based on the selected text."
3. Be accurate and specific
4. Keep answers clear and concise

Selected Text:
{selected_text}

Question: {question}

Answer:"""

        # Gemini se answer generate karo (NO vector search)
        print("Generating answer from selected text...")
        try:
            response = self.model.generate_content(prompt)
            answer = response.text

        except Exception as e:
            print(f"Error generating answer: {e}")
            raise

        return {
            "session_id": session_id or str(uuid.uuid4()),
            "response": answer
        }


# Global service instances
chat_service = ChatService()
selection_chat_service = SelectionChatService()
