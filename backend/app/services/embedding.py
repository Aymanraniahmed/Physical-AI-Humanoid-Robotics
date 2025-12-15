"""
Local embedding service using sentence-transformers
Text ko embeddings (vectors) mein convert karna (FREE, no API limits)
"""

from sentence_transformers import SentenceTransformer
from typing import List
from app.config import settings


class EmbeddingService:
    """
    Local sentence-transformers embeddings (completely free!)
    """

    def __init__(self):
        """Initialize local embedding model"""
        # Load local model (384 dimensions, fast & accurate)
        print("Loading local embedding model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Local embedding model loaded: all-MiniLM-L6-v2 (384-dim)")
        self.embedding_dim = 384  # Model dimension

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Multiple texts ke embeddings generate karo (batch mein)

        Args:
            texts: List of text strings

        Returns:
            List of embedding vectors (har text ke liye ek vector)
        """
        if not texts:
            return []

        try:
            # Local model batch processing (fast!)
            embeddings = self.model.encode(
                texts,
                show_progress_bar=False,
                batch_size=32,
                convert_to_numpy=True
            )

            # Convert to list of lists
            return [emb.tolist() for emb in embeddings]

        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise

    def generate_embedding(self, text: str) -> List[float]:
        """
        Single text ka embedding generate karo

        Args:
            text: Input text string

        Returns:
            Embedding vector (384 dimensions for all-MiniLM-L6-v2)
        """
        try:
            # Local model encoding (fast!)
            embedding = self.model.encode(
                [text],
                show_progress_bar=False,
                convert_to_numpy=True
            )[0]

            return embedding.tolist()

        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise


# Global embedding service instance
embedding_service = EmbeddingService()
