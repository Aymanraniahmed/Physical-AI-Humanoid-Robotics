# Data Model: RAG Chatbot Backend

**Feature**: RAG Chatbot Backend for AI-native Book Platform
**Date**: 2025-12-15
**Version**: 1.0

## Overview

This document defines the data model for the RAG chatbot backend, including entities, relationships, validation rules, and state transitions. The model separates concerns between Postgres (structured metadata, chat history) and Qdrant (vector embeddings).

---

## Entity Definitions

### 1. Book

**Description**: Represents a single book that has been ingested and indexed for RAG queries.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `book_id` | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the book |
| `title` | TEXT | NOT NULL | Book title extracted from metadata or filename |
| `author` | TEXT | NULLABLE | Author name (if available) |
| `source_file_name` | TEXT | NOT NULL | Original uploaded file name (e.g., "physical-ai.pdf") |
| `total_chunks` | INTEGER | NOT NULL, >= 0 | Number of chunks created during ingestion |
| `ingested_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Timestamp of ingestion completion |
| `metadata` | JSONB | NULLABLE | Flexible metadata: `{ "isbn": "...", "publisher": "...", "version": "1.0", "language": "en" }` |

**Validation Rules**:
- `title` must be non-empty string (1-500 chars)
- `source_file_name` must end with .pdf, .html, or .epub
- `total_chunks` must match count of related BookChunk records
- `metadata` must be valid JSON object if provided

**Postgres Schema**:
```sql
CREATE TABLE books (
    book_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL CHECK (char_length(title) BETWEEN 1 AND 500),
    author TEXT CHECK (author IS NULL OR char_length(author) BETWEEN 1 AND 200),
    source_file_name TEXT NOT NULL,
    total_chunks INTEGER NOT NULL CHECK (total_chunks >= 0),
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB
);
```

---

### 2. BookChunk

**Description**: Represents a text segment from a book. Metadata stored in Postgres, embeddings and full text stored in Qdrant.

**Fields (Postgres)**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `chunk_id` | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the chunk |
| `book_id` | UUID | FOREIGN KEY (books), NOT NULL | Reference to parent book |
| `chunk_index` | INTEGER | NOT NULL, >= 0 | Position in book (0-indexed, sequential) |
| `text` | TEXT | NOT NULL | Full chunk text (duplicate of Qdrant payload) |
| `metadata` | JSONB | NULLABLE | `{ "page_number": 42, "chapter": "Introduction", "section": "1.2" }` |

**Fields (Qdrant Payload)**:

| Field | Type | Description |
|-------|------|-------------|
| `book_id` | keyword | For filtering by book |
| `chunk_id` | keyword | UUID as string |
| `chunk_index` | integer | Position in book |
| `text` | text | Full chunk text (for retrieval without DB lookup) |
| `metadata` | object | Same as Postgres `metadata` field |

**Validation Rules**:
- `chunk_index` must be unique per `book_id`
- `text` must be non-empty (1-10000 chars after chunking)
- Embedding vector must be 1536 dimensions (text-embedding-3-small)

**Postgres Schema**:
```sql
CREATE TABLE book_chunks (
    chunk_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id UUID NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL CHECK (chunk_index >= 0),
    text TEXT NOT NULL CHECK (char_length(text) BETWEEN 1 AND 10000),
    metadata JSONB,
    UNIQUE(book_id, chunk_index)
);

CREATE INDEX idx_chunks_book ON book_chunks(book_id);
CREATE INDEX idx_chunks_book_index ON book_chunks(book_id, chunk_index);
```

**Qdrant Collection Config**:
```python
from qdrant_client import models

qdrant_client.create_collection(
    collection_name="physical_ai_book_chunks",
    vectors_config=models.VectorParams(
        size=1536,  # text-embedding-3-small
        distance=models.Distance.COSINE
    ),
    optimizers_config=models.OptimizersConfigDiff(
        indexing_threshold=1000  # Start indexing after 1000 vectors
    )
)

# Create payload index for fast book_id filtering
qdrant_client.create_payload_index(
    collection_name="physical_ai_book_chunks",
    field_name="book_id",
    field_schema=models.PayloadSchemaType.KEYWORD
)
```

---

### 3. ChatSession

**Description**: Represents a conversation session between user and chatbot. Supports both normal RAG and selected-text modes.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `session_id` | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the session |
| `book_id` | UUID | FOREIGN KEY (books), NOT NULL | Book being discussed |
| `mode` | TEXT | CHECK IN ('normal', 'selection'), NOT NULL | Conversation mode |
| `created_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Session creation time |
| `updated_at` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Last message timestamp |
| `metadata` | JSONB | NULLABLE | `{ "user_agent": "...", "ip": "...", "tags": ["debugging"], "archived": false }` |

**Validation Rules**:
- `mode` must be 'normal' (RAG with vector search) or 'selection' (text-only Q&A)
- `updated_at` must be >= `created_at`
- Sessions with no messages for 30 days can be archived (set `metadata.archived = true`)

**State Transitions**:
```
created (0 messages) → active (1+ messages) → archived (optional)
```

**Postgres Schema**:
```sql
CREATE TABLE chat_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id UUID NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
    mode TEXT NOT NULL CHECK (mode IN ('normal', 'selection')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB,
    CHECK (updated_at >= created_at)
);

CREATE INDEX idx_sessions_book ON chat_sessions(book_id);
CREATE INDEX idx_sessions_updated ON chat_sessions(updated_at DESC);

-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION update_session_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_session_timestamp
BEFORE UPDATE ON chat_sessions
FOR EACH ROW EXECUTE FUNCTION update_session_timestamp();
```

---

### 4. Message

**Description**: Represents a single message in a chat session (user query or assistant response).

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `message_id` | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the message |
| `session_id` | UUID | FOREIGN KEY (chat_sessions), NOT NULL | Parent session |
| `role` | TEXT | CHECK IN ('user', 'assistant'), NOT NULL | Message sender |
| `content` | TEXT | NOT NULL | Message text (query or response) |
| `timestamp` | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Message creation time |
| `metadata` | JSONB | NULLABLE | `{ "retrieved_chunks": [{"chunk_id": "...", "score": 0.95}], "model": "gpt-4o-mini", "tokens": 150 }` |

**Validation Rules**:
- `content` must be non-empty (1-50000 chars)
- `role` must alternate in a session (user → assistant → user → ...)
- For `role='assistant'` in 'normal' mode, `metadata.retrieved_chunks` should be populated
- For `role='assistant'` in 'selection' mode, `metadata.selected_text` may be present (from request)

**Metadata Schema** (JSONB):
```typescript
// For assistant messages in 'normal' mode
{
  "retrieved_chunks": [
    {
      "chunk_id": "uuid",
      "text": "snippet...",
      "score": 0.95,  // Qdrant similarity score
      "metadata": { "page_number": 42 }
    }
  ],
  "model": "gpt-4o-mini",
  "prompt_tokens": 1200,
  "completion_tokens": 150,
  "total_tokens": 1350
}

// For assistant messages in 'selection' mode
{
  "selected_text": "text user highlighted",
  "model": "gpt-4o-mini",
  "prompt_tokens": 800,
  "completion_tokens": 100,
  "total_tokens": 900
}
```

**Postgres Schema**:
```sql
CREATE TABLE messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL CHECK (char_length(content) BETWEEN 1 AND 50000),
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB
);

CREATE INDEX idx_messages_session ON messages(session_id, timestamp ASC);
CREATE INDEX idx_messages_session_desc ON messages(session_id, timestamp DESC);
```

---

## Relationships

### Entity-Relationship Diagram

```
┌─────────────┐
│   Book      │
│ (book_id)   │
└──────┬──────┘
       │ 1
       │
       │ N
┌──────┴──────────┐         ┌─────────────────┐
│  BookChunk      │         │  Qdrant Cloud   │
│ (chunk_id)      │────────▶│  (embeddings)   │
│ - book_id (FK)  │         │  + payload      │
└─────────────────┘         └─────────────────┘

┌─────────────┐
│   Book      │
│ (book_id)   │
└──────┬──────┘
       │ 1
       │
       │ N
┌──────┴──────────┐
│  ChatSession    │
│ (session_id)    │
│ - book_id (FK)  │
└──────┬──────────┘
       │ 1
       │
       │ N
┌──────┴──────────┐
│   Message       │
│ (message_id)    │
│ - session_id FK │
└─────────────────┘
```

### Relationship Details

1. **Book ↔ BookChunk** (1:N)
   - One book has many chunks
   - CASCADE DELETE: Deleting book deletes all chunks
   - Chunk order: `chunk_index` maintains sequential position

2. **Book ↔ ChatSession** (1:N)
   - One book can have many chat sessions
   - CASCADE DELETE: Deleting book deletes all sessions
   - Sessions are scoped to a single book (no cross-book conversations in MVP)

3. **ChatSession ↔ Message** (1:N)
   - One session has many messages
   - CASCADE DELETE: Deleting session deletes all messages
   - Messages ordered by `timestamp` ASC for conversation replay

4. **BookChunk ↔ Qdrant** (1:1)
   - Each chunk has one embedding vector in Qdrant
   - Linked by `chunk_id` (stored in Qdrant payload)
   - Qdrant is source of truth for embeddings; Postgres stores metadata

---

## Data Storage Strategy

### Postgres (Neon Serverless)

**Purpose**: Structured metadata, relational data, chat history

**Stored Data**:
- Book metadata (title, author, file name)
- Chunk metadata (text, page numbers, chapters)
- Chat sessions (mode, timestamps)
- Conversation history (messages)

**Why Postgres**:
- ACID transactions (e.g., ingest book + chunks atomically)
- Rich querying (JOIN sessions with messages)
- JSONB for schema flexibility
- Neon serverless auto-scales with usage

### Qdrant (Cloud)

**Purpose**: Vector embeddings, semantic search

**Stored Data**:
- Chunk embeddings (1536-dim vectors)
- Chunk text (payload, for retrieval without DB lookup)
- Metadata (book_id, chunk_id, page numbers)

**Why Qdrant**:
- Optimized for vector similarity search (cosine distance)
- Fast retrieval (<50ms p95 for 1000s of vectors)
- Payload filtering (e.g., filter by book_id)
- Cloud-native scaling

### Data Consistency

**Ingestion Flow** (ensure consistency):
```python
async def ingest_book(file: UploadFile, book_id: UUID | None) -> Book:
    async with db.transaction():  # Postgres transaction
        # 1. Create/update book record
        book = await db.save_book(book_id, title, author, total_chunks)

        # 2. Save chunk metadata to Postgres
        await db.save_chunks(book_id, chunks)

    # 3. Upsert embeddings to Qdrant (separate from transaction)
    await qdrant.upsert_chunks(book_id, chunks, embeddings)

    return book
```

**Deletion Flow** (cascade cleanup):
```python
async def delete_book(book_id: UUID):
    # 1. Delete from Qdrant (manual, no foreign keys)
    await qdrant.delete_by_filter(book_id=book_id)

    # 2. Delete from Postgres (cascades to chunks, sessions, messages)
    await db.delete_book(book_id)
```

---

## Validation Rules Summary

### Book
- ✅ Title: 1-500 chars, non-empty
- ✅ File name: Must end with .pdf, .html, .epub
- ✅ Total chunks: Must match BookChunk count

### BookChunk
- ✅ Chunk index: Unique per book, sequential
- ✅ Text: 1-10000 chars (post-chunking)
- ✅ Embedding: 1536 dimensions (validated by Qdrant)

### ChatSession
- ✅ Mode: Must be 'normal' or 'selection'
- ✅ Timestamps: updated_at >= created_at
- ✅ Book reference: Must exist in books table

### Message
- ✅ Role: Must be 'user' or 'assistant'
- ✅ Content: 1-50000 chars
- ✅ Role alternation: user → assistant → user (enforced at API level)
- ✅ Metadata: Valid JSON, schema depends on mode

---

## Pydantic Models (API Layer)

### Request/Response Schemas

```python
from pydantic import BaseModel, Field, validator
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Literal

# ---------- Book Models ----------

class BookMetadata(BaseModel):
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    version: Optional[str] = None
    language: str = "en"

class BookResponse(BaseModel):
    book_id: UUID
    title: str
    author: Optional[str] = None
    source_file_name: str
    total_chunks: int
    ingested_at: datetime
    metadata: Optional[BookMetadata] = None

# ---------- Chunk Models ----------

class ChunkMetadata(BaseModel):
    page_number: Optional[int] = None
    chapter: Optional[str] = None
    section: Optional[str] = None

class ChunkSource(BaseModel):
    chunk_id: UUID
    text: str = Field(..., max_length=500)  # Truncated for API response
    score: float = Field(..., ge=0.0, le=1.0)
    metadata: Optional[ChunkMetadata] = None

# ---------- Chat Models ----------

class ChatRequest(BaseModel):
    session_id: Optional[UUID] = None  # Null = new session
    book_id: UUID
    message: str = Field(..., min_length=1, max_length=5000)

class ChatResponse(BaseModel):
    session_id: UUID
    response: str
    sources: List[ChunkSource] = Field(default_factory=list)
    timestamp: datetime

class SelectionChatRequest(BaseModel):
    session_id: Optional[UUID] = None
    selected_text: str = Field(..., min_length=1, max_length=10000)
    question: str = Field(..., min_length=1, max_length=5000)

class SelectionChatResponse(BaseModel):
    session_id: UUID
    response: str
    timestamp: datetime

# ---------- Ingest Models ----------

class IngestRequest(BaseModel):
    book_id: Optional[UUID] = None  # Null = new book, existing = re-ingest
    metadata: Optional[BookMetadata] = None

class IngestResponse(BaseModel):
    book_id: UUID
    title: str
    total_chunks: int
    status: Literal["completed", "failed"]
    error: Optional[str] = None

# ---------- Health Check ----------

class ServiceStatus(BaseModel):
    postgres: Literal["up", "down"]
    qdrant: Literal["up", "down"]
    openai: Literal["up", "down"]

class HealthResponse(BaseModel):
    status: Literal["healthy", "degraded", "unhealthy"]
    services: ServiceStatus
    timestamp: datetime
```

---

## State Transitions

### ChatSession Lifecycle

```
┌─────────────┐
│   CREATED   │  (session_id generated, 0 messages)
└──────┬──────┘
       │ POST /chat or /chat/selection
       ▼
┌─────────────┐
│   ACTIVE    │  (1+ messages, updated_at refreshed on each message)
└──────┬──────┘
       │ No messages for 30 days (optional)
       ▼
┌─────────────┐
│  ARCHIVED   │  (metadata.archived = true, read-only)
└─────────────┘
```

**Transitions**:
- **CREATED → ACTIVE**: First user message added
- **ACTIVE → ACTIVE**: Each new message updates `updated_at`
- **ACTIVE → ARCHIVED**: Manual archival or auto-archive policy (future)

---

## Migration Strategy

### Initial Schema Setup

Using Alembic for migrations:

```python
# alembic/versions/001_initial_schema.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

def upgrade():
    # Books table
    op.create_table(
        'books',
        sa.Column('book_id', UUID(), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('author', sa.Text(), nullable=True),
        sa.Column('source_file_name', sa.Text(), nullable=False),
        sa.Column('total_chunks', sa.Integer(), nullable=False),
        sa.Column('ingested_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('metadata', JSONB(), nullable=True),
        sa.CheckConstraint('char_length(title) BETWEEN 1 AND 500', name='check_title_length'),
        sa.CheckConstraint('total_chunks >= 0', name='check_chunks_nonnegative')
    )

    # BookChunks table (similar pattern)
    # ChatSessions table (similar pattern)
    # Messages table (similar pattern)

    # Indexes
    op.create_index('idx_chunks_book', 'book_chunks', ['book_id'])
    op.create_index('idx_sessions_book', 'chat_sessions', ['book_id'])
    op.create_index('idx_messages_session', 'messages', ['session_id', 'timestamp'])

def downgrade():
    op.drop_table('messages')
    op.drop_table('chat_sessions')
    op.drop_table('book_chunks')
    op.drop_table('books')
```

---

## Performance Considerations

### Indexing Strategy

1. **book_chunks**: Index on `(book_id, chunk_index)` for fast chunk retrieval in order
2. **chat_sessions**: Index on `book_id` for listing sessions, `updated_at DESC` for recent sessions
3. **messages**: Composite index on `(session_id, timestamp ASC)` for conversation replay

### Query Patterns

**Load recent conversation history** (most common):
```sql
SELECT role, content, timestamp, metadata
FROM messages
WHERE session_id = $1
ORDER BY timestamp DESC
LIMIT 10;
```

**Retrieve chunks for a book** (for admin/debugging):
```sql
SELECT chunk_id, chunk_index, text, metadata
FROM book_chunks
WHERE book_id = $1
ORDER BY chunk_index ASC;
```

**Count messages per session** (analytics):
```sql
SELECT session_id, COUNT(*) as message_count
FROM messages
GROUP BY session_id;
```

---

## Security & Privacy

### Data Retention

- **Messages**: Keep indefinitely (for conversation continuity), allow user-initiated deletion
- **Sessions**: Archive after 30 days of inactivity (soft delete: `metadata.archived = true`)
- **Books**: Keep until explicitly deleted by admin

### PII Handling

- No user authentication in MVP → no PII stored
- Future: If adding user accounts, encrypt user metadata, anonymize IP addresses

### Access Control

- Future: Add `user_id` foreign key to `chat_sessions` for multi-tenancy
- Future: Row-level security (RLS) in Postgres to isolate user data

---

**Status**: Data model complete
**Next**: Generate API contracts (`contracts/api.openapi.yaml`)
