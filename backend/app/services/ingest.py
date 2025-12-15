"""
Book ingestion service
Document upload, parse, chunk, embed, aur store
"""

from typing import Tuple
import uuid
from app.utils.parsers import parse_document
from app.utils.chunking import chunk_document_with_metadata
from app.services.embedding import embedding_service
from app.services.vector_store import vector_store


class IngestService:
    """
    Book ingestion pipeline
    File -> Parse -> Chunk -> Embed -> Store in Qdrant
    """

    def ingest_book(
        self,
        file_content: bytes,
        filename: str,
        book_id: str = None
    ) -> dict:
        """
        Complete book ingestion pipeline

        Args:
            file_content: File ka binary content
            filename: File ka naam (extension detect karne ke liye)
            book_id: Optional book ID (nahi diya toh auto-generate hoga)

        Returns:
            Dict with book_id, title, total_chunks, status
        """

        # Book ID generate karo agar nahi diya
        if not book_id:
            book_id = str(uuid.uuid4())

        print(f"\n{'='*50}")
        print(f"Starting book ingestion for: {filename}")
        print(f"Book ID: {book_id}")
        print(f"{'='*50}\n")

        try:
            # Step 1: Document parse karo (PDF/HTML/EPUB)
            print("Step 1: Parsing document...")
            text, metadata = parse_document(file_content, filename)
            print(f"✓ Parsed successfully! Title: {metadata.get('title', 'Unknown')}")

            # Step 2: Text ko chunks mein todo
            print("\nStep 2: Chunking text...")
            chunks = chunk_document_with_metadata(text, metadata)
            print(f"✓ Created {len(chunks)} chunks")

            # Step 3: Har chunk ke liye embedding generate karo
            print("\nStep 3: Generating embeddings...")
            chunk_texts = [chunk["text"] for chunk in chunks]

            # Batches mein embeddings generate karo (cost bachane ke liye)
            batch_size = 50
            all_embeddings = []

            for i in range(0, len(chunk_texts), batch_size):
                batch = chunk_texts[i:i + batch_size]
                print(f"  Embedding batch {i//batch_size + 1}/{(len(chunk_texts)-1)//batch_size + 1}...")
                embeddings = embedding_service.generate_embeddings(batch)
                all_embeddings.extend(embeddings)

            print(f"✓ Generated {len(all_embeddings)} embeddings")

            # Step 4: Qdrant mein upload karo
            print("\nStep 4: Uploading to Qdrant...")
            vector_store.upsert_chunks(
                book_id=book_id,
                chunks=chunks,
                embeddings=all_embeddings
            )
            print(f"✓ Uploaded to Qdrant successfully!")

            print(f"\n{'='*50}")
            print("Book ingestion completed successfully!")
            print(f"{'='*50}\n")

            return {
                "book_id": book_id,
                "title": metadata.get("title", filename),
                "total_chunks": len(chunks),
                "status": "completed",
                "message": f"Successfully ingested {len(chunks)} chunks"
            }

        except Exception as e:
            print(f"\n✗ Error during ingestion: {e}")
            return {
                "book_id": book_id,
                "title": filename,
                "total_chunks": 0,
                "status": "failed",
                "message": str(e)
            }


# Global ingest service instance
ingest_service = IngestService()
