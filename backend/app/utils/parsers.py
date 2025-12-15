"""
Document parsers - PDF, HTML, EPUB
Har format se text extract karna
"""

import io
from typing import Tuple
from pypdf import PdfReader
import pdfplumber
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub


def parse_pdf(file_content: bytes) -> Tuple[str, dict]:
    """
    PDF se text extract karo

    Args:
        file_content: PDF file ka binary content

    Returns:
        (extracted_text, metadata)
    """
    text = ""
    metadata = {"page_count": 0, "title": "Unknown", "file_type": "pdf"}

    try:
        # Pehle pypdf try karo (fast hai)
        pdf_file = io.BytesIO(file_content)
        reader = PdfReader(pdf_file)

        metadata["page_count"] = len(reader.pages)

        # Metadata extract karo
        if reader.metadata:
            metadata["title"] = reader.metadata.get("/Title", "Unknown")
            metadata["author"] = reader.metadata.get("/Author", "Unknown")

        # Har page se text nikalo
        for page_num, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            if page_text:
                text += f"\n--- Page {page_num} ---\n{page_text}"

    except Exception as e:
        # Agar pypdf fail ho toh pdfplumber try karo
        print(f"pypdf failed, trying pdfplumber: {e}")
        try:
            pdf_file = io.BytesIO(file_content)
            with pdfplumber.open(pdf_file) as pdf:
                metadata["page_count"] = len(pdf.pages)
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {page_num} ---\n{page_text}"
        except Exception as e2:
            raise Exception(f"PDF parsing failed: {e2}")

    return text.strip(), metadata


def parse_html(file_content: bytes) -> Tuple[str, dict]:
    """
    HTML se text extract karo

    Args:
        file_content: HTML file ka binary content

    Returns:
        (extracted_text, metadata)
    """
    try:
        html_text = file_content.decode('utf-8')
        soup = BeautifulSoup(html_text, 'lxml')

        # Title extract karo
        title = soup.find('title')
        title_text = title.get_text() if title else "Unknown"

        # Script aur style tags hata do
        for script in soup(["script", "style"]):
            script.decompose()

        # Text extract karo
        text = soup.get_text()

        # Extra whitespace clean karo
        lines = (line.strip() for line in text.splitlines())
        text = '\n'.join(line for line in lines if line)

        metadata = {
            "title": title_text,
            "file_type": "html"
        }

        return text, metadata

    except Exception as e:
        raise Exception(f"HTML parsing failed: {e}")


def parse_epub(file_content: bytes) -> Tuple[str, dict]:
    """
    EPUB (ebook) se text extract karo

    Args:
        file_content: EPUB file ka binary content

    Returns:
        (extracted_text, metadata)
    """
    try:
        book = epub.read_epub(io.BytesIO(file_content))

        # Metadata extract karo
        title = book.get_metadata('DC', 'title')
        author = book.get_metadata('DC', 'creator')

        metadata = {
            "title": title[0][0] if title else "Unknown",
            "author": author[0][0] if author else "Unknown",
            "file_type": "epub"
        }

        # Saare chapters se text nikalo
        text = ""
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                # HTML content ko parse karo
                soup = BeautifulSoup(item.get_content(), 'lxml')
                text += "\n" + soup.get_text() + "\n"

        return text.strip(), metadata

    except Exception as e:
        raise Exception(f"EPUB parsing failed: {e}")


def parse_document(file_content: bytes, filename: str) -> Tuple[str, dict]:
    """
    File type detect karke appropriate parser use karo

    Args:
        file_content: File ka binary content
        filename: File ka naam (extension check karne ke liye)

    Returns:
        (extracted_text, metadata)
    """
    filename_lower = filename.lower()

    if filename_lower.endswith('.pdf'):
        return parse_pdf(file_content)
    elif filename_lower.endswith('.html') or filename_lower.endswith('.htm'):
        return parse_html(file_content)
    elif filename_lower.endswith('.epub'):
        return parse_epub(file_content)
    else:
        raise ValueError(f"Unsupported file format: {filename}. Only PDF, HTML, EPUB supported.")
