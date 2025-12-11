"""
Script to index book documents into Qdrant vector database.

This script:
1. Scans the docs directory for markdown files
2. Chunks them into ~1000 character pieces with overlap
3. Generates embeddings using OpenAI
4. Uploads vectors to Qdrant Cloud
"""

import os
import sys
from pathlib import Path
from typing import List, Dict
import re

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant_client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# Configuration
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "book_chunks")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
DOCS_DIR = Path(__file__).parent.parent.parent / "Physical-AI-Humanoid-Robotics-" / "docs"


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks


def extract_metadata(file_path: Path, content: str) -> Dict[str, str]:
    """Extract chapter and section from file path and content."""
    # Extract chapter from directory structure
    parts = file_path.parts
    chapter = "Unknown"
    for part in parts:
        if part.startswith("module-"):
            chapter = part.replace("-", " ").title()
        elif part in ["intro", "foundations", "capstone"]:
            chapter = part.title()

    # Extract section from filename
    section = file_path.stem.replace("-", " ").title()

    return {
        "chapter": chapter,
        "section": section,
        "file": str(file_path.relative_to(DOCS_DIR))
    }


def get_markdown_files(docs_dir: Path) -> List[Path]:
    """Get all markdown files from docs directory."""
    return list(docs_dir.rglob("*.md"))


def process_file(file_path: Path) -> List[Dict]:
    """Process a single markdown file into chunks with metadata."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract metadata
    metadata = extract_metadata(file_path, content)

    # Chunk the content
    chunks = chunk_text(content)

    # Create chunk objects
    chunk_objects = []
    for i, chunk in enumerate(chunks):
        chunk_obj = {
            "text": chunk,
            "metadata": {
                **metadata,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
        }
        chunk_objects.append(chunk_obj)

    return chunk_objects


def get_embedding(text: str) -> List[float]:
    """Get embedding for text using OpenAI."""
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


def create_collection():
    """Create Qdrant collection if it doesn't exist."""
    try:
        qdrant_client.get_collection(COLLECTION_NAME)
        print(f"✓ Collection '{COLLECTION_NAME}' already exists")
    except Exception:
        print(f"Creating collection '{COLLECTION_NAME}'...")
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
        print("✓ Collection created")


def upload_chunks(chunks: List[Dict]):
    """Upload chunks with embeddings to Qdrant."""
    points = []

    print(f"\nGenerating embeddings and preparing upload...")
    for i, chunk in enumerate(chunks):
        if i % 10 == 0:
            print(f"  Processing chunk {i + 1}/{len(chunks)}...")

        # Get embedding
        embedding = get_embedding(chunk["text"])

        # Create point
        point = PointStruct(
            id=i,
            vector=embedding,
            payload={
                "text": chunk["text"],
                "chapter": chunk["metadata"]["chapter"],
                "section": chunk["metadata"]["section"],
                "file": chunk["metadata"]["file"],
                "chunk_index": chunk["metadata"]["chunk_index"]
            }
        )
        points.append(point)

    # Upload to Qdrant
    print(f"\nUploading {len(points)} chunks to Qdrant...")
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    print("✓ Upload complete!")


def main():
    """Main indexing function."""
    print("=" * 60)
    print("Physical AI Book - Document Indexing")
    print("=" * 60)

    # Check docs directory
    if not DOCS_DIR.exists():
        print(f"❌ Error: Docs directory not found at {DOCS_DIR}")
        sys.exit(1)

    # Get markdown files
    print(f"\nScanning docs directory: {DOCS_DIR}")
    md_files = get_markdown_files(DOCS_DIR)
    print(f"✓ Found {len(md_files)} markdown files")

    # Process all files
    print("\nProcessing files...")
    all_chunks = []
    for file_path in md_files:
        print(f"  • {file_path.name}")
        chunks = process_file(file_path)
        all_chunks.extend(chunks)
        print(f"    → {len(chunks)} chunks")

    print(f"\n✓ Total chunks created: {len(all_chunks)}")

    # Create collection
    print("\nSetting up Qdrant collection...")
    create_collection()

    # Upload chunks
    upload_chunks(all_chunks)

    print("\n" + "=" * 60)
    print("✓ Indexing complete!")
    print("=" * 60)
    print(f"\nCollection: {COLLECTION_NAME}")
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Embedding model: {EMBEDDING_MODEL}")


if __name__ == "__main__":
    main()
