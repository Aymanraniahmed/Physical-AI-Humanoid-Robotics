"""
Book ingestion API endpoint
POST /ingest/book - Book upload karne ke liye
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
from app.services.ingest import ingest_service
from app.models.book import IngestResponse


router = APIRouter(
    prefix="/ingest",
    tags=["Book Ingestion"]
)


@router.post("/book", response_model=IngestResponse)
async def upload_book(
    file: UploadFile = File(..., description="Book file (PDF/HTML/EPUB)"),
    book_id: Optional[str] = Form(None, description="Optional book ID"),
):
    """
    Book upload aur process karo

    - **file**: PDF, HTML, ya EPUB file
    - **book_id**: Optional - agar nahi diya toh auto-generate hoga

    Process:
    1. File validate karo
    2. Parse karo (text extract karo)
    3. Chunks banao
    4. Embeddings generate karo
    5. Qdrant mein store karo

    Returns:
    - book_id
    - title
    - total_chunks
    - status (completed/failed)
    """

    # File type validate karo
    allowed_extensions = ['.pdf', '.html', '.htm', '.epub']
    file_extension = None

    for ext in allowed_extensions:
        if file.filename.lower().endswith(ext):
            file_extension = ext
            break

    if not file_extension:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file format. Only PDF, HTML, EPUB are supported. Got: {file.filename}"
        )

    try:
        # File content read karo
        file_content = await file.read()

        # Ingest service call karo
        result = ingest_service.ingest_book(
            file_content=file_content,
            filename=file.filename,
            book_id=book_id
        )

        # Response return karo
        return IngestResponse(**result)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing book: {str(e)}"
        )
