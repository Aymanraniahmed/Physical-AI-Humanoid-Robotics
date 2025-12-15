"""
Text chunking utilities
Badi text ko chhote chunks mein todna
"""

import tiktoken
from typing import List
from app.config import settings


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """
    Text mein kitne tokens hain ye count karo

    Args:
        text: Input text
        model: Model name (token counting ke liye)

    Returns:
        Token count
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")  # Default encoding

    return len(encoding.encode(text))


def chunk_text(
    text: str,
    chunk_size: int = None,
    chunk_overlap: int = None,
    model: str = "gpt-4"
) -> List[str]:
    """
    Text ko chunks mein todo with overlap

    Example:
        text = "Yeh ek lambi text hai jo chunks mein todne ki zaroorat hai..."
        chunks = chunk_text(text, chunk_size=1000, chunk_overlap=200)

    Args:
        text: Input text to chunk
        chunk_size: Har chunk mein kitne tokens (default: config se)
        chunk_overlap: Chunks ke beech overlap (default: config se)
        model: Model name for token counting

    Returns:
        List of text chunks
    """
    # Default values config se lo
    if chunk_size is None:
        chunk_size = settings.chunk_size
    if chunk_overlap is None:
        chunk_overlap = settings.chunk_overlap

    # Tokenizer setup
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    # Text ko tokens mein convert karo
    tokens = encoding.encode(text)

    chunks = []
    start = 0

    while start < len(tokens):
        # Current chunk ke tokens
        end = start + chunk_size
        chunk_tokens = tokens[start:end]

        # Tokens ko text mein wapas convert karo
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)

        # Next chunk ka start = current_end - overlap
        # Overlap se chunks ke beech continuity bani rahegi
        start = end - chunk_overlap

        # Agar overlap se start negative ho gaya toh break
        if start >= len(tokens):
            break

    return chunks


def chunk_document_with_metadata(
    text: str,
    metadata: dict,
    chunk_size: int = None,
    chunk_overlap: int = None
) -> List[dict]:
    """
    Document ko chunks mein todo aur har chunk ke saath metadata attach karo

    Args:
        text: Document text
        metadata: Document metadata (title, author, etc.)
        chunk_size: Chunk size in tokens
        chunk_overlap: Overlap between chunks

    Returns:
        List of dicts with 'text' and 'metadata' keys
    """
    # Text ko chunks mein todo
    text_chunks = chunk_text(text, chunk_size, chunk_overlap)

    # Har chunk ke saath metadata attach karo
    chunks_with_metadata = []
    for idx, chunk_text in enumerate(text_chunks):
        chunk_data = {
            "text": chunk_text,
            "chunk_index": idx,
            "metadata": {
                **metadata,  # Original metadata
                "chunk_index": idx,
                "total_chunks": len(text_chunks),
                "token_count": count_tokens(chunk_text)
            }
        }
        chunks_with_metadata.append(chunk_data)

    return chunks_with_metadata
