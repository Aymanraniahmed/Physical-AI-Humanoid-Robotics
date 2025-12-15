"""
Startup script to auto-load the book into vector database
Book automatically ready hogi - user ko upload karne ki zaroorat nahi
"""

import os
import uuid
from pathlib import Path
from app.utils import chunking
from app.services.embedding import embedding_service
from app.services.vector_store import vector_store
from qdrant_client.models import PointStruct


def auto_load_book():
    """
    Startup pe book automatically load kar do
    Taake user seedha questions pooch sake
    """
    print("\n" + "="*60)
    print("AUTO-LOADING BOOK INTO VECTOR DATABASE")
    print("="*60)

    # Book path
    book_path = Path("sample-book.txt")

    if not book_path.exists():
        print(f"[WARNING] Book not found at {book_path}")
        print("[INFO] Chatbot will not have book context")
        return None

    try:
        # 1. Load book
        print(f"\n[1/4] Loading book from {book_path}...")
        with open(book_path, 'r', encoding='utf-8') as f:
            book_text = f.read()
        print(f"[OK] Book loaded: {len(book_text)} characters")

        # 2. Chunk text
        print("\n[2/4] Chunking text...")
        chunks = chunking.chunk_text(
            book_text,
            chunk_size=1000,
            chunk_overlap=200
        )
        print(f"[OK] Created {len(chunks)} chunks")

        # 3. Generate embeddings
        print("\n[3/4] Generating embeddings (local model)...")
        # chunks is already a list of strings from chunk_text()
        embeddings = embedding_service.generate_embeddings(chunks)
        print(f"[OK] Generated {len(embeddings)} embeddings")

        # 4. Store in Qdrant
        print("\n[4/4] Storing in vector database...")

        # Create points (using UUID strings for Qdrant compatibility)
        points = []
        for i, (chunk_str, embedding) in enumerate(zip(chunks, embeddings)):
            point = PointStruct(
                id=str(uuid.uuid4()),  # Use UUID string instead of integer
                vector=embedding,
                payload={
                    'text': chunk_str,  # chunk is already a string
                    'metadata': {},  # No metadata for simple chunks
                    'book_id': 'default',  # Fixed book ID
                    'chunk_index': i
                }
            )
            points.append(point)

        # Upload to Qdrant
        vector_store.client.upsert(
            collection_name=vector_store.collection_name,
            points=points
        )

        print(f"[OK] Stored {len(points)} vectors in Qdrant")
        print("\n" + "="*60)
        print("[SUCCESS] BOOK AUTO-LOADED SUCCESSFULLY!")
        print("[READY] Chatbot ready to answer questions!")
        print("="*60 + "\n")

        return 'default'  # Return default book_id

    except Exception as e:
        print(f"\n[ERROR] Failed to auto-load book: {e}")
        print("[INFO] Chatbot will not have book context")
        import traceback
        traceback.print_exc()
        return None


# Global variable to store book_id
DEFAULT_BOOK_ID = None

def get_default_book_id():
    """Get the auto-loaded book ID"""
    return DEFAULT_BOOK_ID or 'default'
