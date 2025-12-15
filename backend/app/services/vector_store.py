"""
Qdrant vector store operations
Embeddings store karna aur search karna
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from typing import List, Dict, Any
from app.config import settings
import uuid


class VectorStore:
    """
    Qdrant vector database ke saath interact karne ke liye class
    """

    def __init__(self):
        """Initialize Qdrant client"""
        # Qdrant client setup
        # Check if using in-memory or remote Qdrant
        if settings.qdrant_url == ":memory:":
            # In-memory Qdrant (no Docker needed!)
            self.client = QdrantClient(":memory:")
            print("Using in-memory Qdrant (no Docker required)")
        else:
            # Remote Qdrant (Docker or Cloud)
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key if settings.qdrant_api_key else None
            )
            print(f"Using Qdrant at: {settings.qdrant_url}")

        self.collection_name = settings.qdrant_collection_name

        # Collection create karo agar exist nahi karta
        self._create_collection_if_not_exists()

    def _create_collection_if_not_exists(self):
        """
        Qdrant collection banao agar pehle se nahi hai
        Collection = database ki table jaise
        """
        try:
            # Check karo ke collection exist karta hai ya nahi
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name not in collection_names:
                print(f"Creating collection: {self.collection_name}")

                # Collection banao with vector configuration
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=settings.embedding_dimension,  # 1536 for text-embedding-3-small
                        distance=Distance.COSINE  # Cosine similarity use karenge
                    )
                )
                print(f"Collection '{self.collection_name}' created successfully!")
            else:
                print(f"Collection '{self.collection_name}' already exists.")

        except Exception as e:
            print(f"Error creating collection: {e}")
            raise

    def upsert_chunks(self, book_id: str, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        """
        Book chunks aur unke embeddings ko Qdrant mein store karo

        Args:
            book_id: Book ka unique ID
            chunks: List of chunk dicts with text and metadata
            embeddings: List of embedding vectors (har chunk ke liye ek)
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Chunks aur embeddings ki length same honi chahiye")

        # Qdrant points banao
        points = []
        for chunk, embedding in zip(chunks, embeddings):
            point_id = str(uuid.uuid4())  # Unique ID har point ke liye

            # Payload mein text aur metadata store karo
            payload = {
                "book_id": book_id,
                "text": chunk["text"],
                "chunk_index": chunk["chunk_index"],
                "metadata": chunk.get("metadata", {})
            }

            # Point create karo
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload=payload
            )
            points.append(point)

        # Qdrant mein upload karo (batch mein fast hoga)
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        print(f"Uploaded {len(points)} chunks to Qdrant for book_id: {book_id}")

    def search(
        self,
        query_embedding: List[float],
        book_id: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Query embedding ke basis par similar chunks search karo

        Args:
            query_embedding: Query ka embedding vector
            book_id: Kis book mein search karna hai
            limit: Kitne top results chahiye

        Returns:
            List of matching chunks with scores
        """
        # Filter lagao - sirf is book_id ke chunks mein search karo
        search_filter = Filter(
            must=[
                FieldCondition(
                    key="book_id",
                    match=MatchValue(value=book_id)
                )
            ]
        )

        # Vector search karo (using query_points in qdrant-client 1.16+)
        query_response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            query_filter=search_filter,
            limit=limit
        )

        # Results ko readable format mein convert karo
        results = []
        for hit in query_response.points:
            result = {
                "chunk_id": hit.id,
                "text": hit.payload.get("text", ""),
                "score": hit.score,  # Similarity score (0-1)
                "metadata": hit.payload.get("metadata", {})
            }
            results.append(result)

        return results

    def delete_by_book_id(self, book_id: str):
        """
        Ek book ke saare chunks delete karo

        Args:
            book_id: Book ka ID jiske chunks delete karne hain
        """
        # Book ID ke basis par filter karo aur delete karo
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="book_id",
                        match=MatchValue(value=book_id)
                    )
                ]
            )
        )
        print(f"Deleted all chunks for book_id: {book_id}")

    def health_check(self) -> bool:
        """
        Check karo ke Qdrant working hai ya nahi

        Returns:
            True if healthy, False otherwise
        """
        try:
            collections = self.client.get_collections()
            return True
        except Exception as e:
            print(f"Qdrant health check failed: {e}")
            return False


# Global vector store instance
# Import karke use karo: from app.services.vector_store import vector_store
vector_store = VectorStore()
