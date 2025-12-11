"""RAG (Retrieval-Augmented Generation) service for the chatbot."""

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Tuple, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime

from .config import settings


class RAGService:
    """Service for Retrieval-Augmented Generation using OpenAI, Qdrant, and Postgres."""

    def __init__(self):
        """Initialize RAG service with OpenAI, Qdrant, and Postgres clients."""
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        self.qdrant_client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key
        )
        self.db_url = settings.database_url

    def _get_db_connection(self):
        """Get database connection."""
        return psycopg2.connect(self.db_url)

    async def get_answer(
        self,
        query: str,
        selected_text: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> Tuple[str, List[Dict]]:
        """
        Get an answer to a query using RAG.

        Args:
            query: User's question
            selected_text: Optional text selected by user
            session_id: Session ID for history tracking

        Returns:
            Tuple of (answer, sources)
        """
        # If selected text provided, use it as context directly
        if selected_text:
            context = selected_text
            sources = [{"chapter": "Selected Text", "section": "User Selection", "score": 1.0}]
        else:
            # Otherwise, retrieve relevant chunks from Qdrant
            query_vector = self._get_embedding(query)
            search_results = self.qdrant_client.search(
                collection_name=settings.qdrant_collection,
                query_vector=query_vector,
                limit=settings.top_k_results
            )

            # Extract context and sources
            context = "\n\n".join([hit.payload["text"] for hit in search_results])
            sources = [
                {
                    "chapter": hit.payload.get("chapter", "Unknown"),
                    "section": hit.payload.get("section", "Unknown"),
                    "score": float(hit.score)
                }
                for hit in search_results
            ]

        # Generate answer using OpenAI
        answer = self._generate_answer(query, context)

        # Save to chat history
        if session_id:
            self._save_message(session_id, "user", query)
            self._save_message(session_id, "assistant", answer)

        return answer, sources

    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding for text using OpenAI."""
        response = self.openai_client.embeddings.create(
            model=settings.embedding_model,
            input=text
        )
        return response.data[0].embedding

    def _generate_answer(self, query: str, context: str) -> str:
        """Generate answer using OpenAI GPT-4."""
        system_prompt = """You are an expert assistant for the "Physical AI & Humanoid Robotics" book.
Your role is to answer questions accurately based on the provided context from the book.

Guidelines:
- Answer based only on the provided context
- Be clear, concise, and technical when appropriate
- If the context doesn't contain enough information, say so
- Use examples from the book when relevant
- Format code snippets properly
- Maintain a helpful, educational tone"""

        user_prompt = f"""Context from the book:
{context}

Question: {query}

Please provide a detailed answer based on the context above."""

        response = self.openai_client.chat.completions.create(
            model=settings.chat_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        return response.choices[0].message.content

    def _save_message(self, session_id: str, role: str, content: str):
        """Save message to database."""
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()

            # Create table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id SERIAL PRIMARY KEY,
                    session_id VARCHAR(255) NOT NULL,
                    role VARCHAR(50) NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Insert message
            cursor.execute(
                """
                INSERT INTO chat_history (session_id, role, content)
                VALUES (%s, %s, %s)
                """,
                (session_id, role, content)
            )

            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error saving message: {e}")

    async def get_session_history(self, session_id: str) -> List[Dict]:
        """Get chat history for a session."""
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)

            cursor.execute(
                """
                SELECT role, content, timestamp
                FROM chat_history
                WHERE session_id = %s
                ORDER BY timestamp ASC
                """,
                (session_id,)
            )

            history = cursor.fetchall()
            cursor.close()
            conn.close()

            return [dict(row) for row in history]
        except Exception as e:
            print(f"Error getting history: {e}")
            return []

    async def clear_session(self, session_id: str):
        """Clear chat history for a session."""
        try:
            conn = self._get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM chat_history WHERE session_id = %s",
                (session_id,)
            )

            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"Error clearing session: {e}")
