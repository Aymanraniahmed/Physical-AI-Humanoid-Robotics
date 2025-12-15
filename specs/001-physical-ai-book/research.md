# Research: RAG Chatbot Backend Technology Decisions

**Feature**: RAG Chatbot Backend for AI-native Book Platform
**Date**: 2025-12-15
**Status**: Phase 0 Complete

## Overview

This document captures research findings and technology decisions for building a production-ready RAG chatbot backend. Each decision includes the chosen approach, rationale, alternatives considered, and references.

---

## 1. Document Parsing Strategy

### Decision: Multi-library approach with fallback chain

**Chosen Stack**:
- **PDF**: pypdf (primary), pdfplumber (fallback for complex layouts)
- **EPUB**: ebooklib
- **HTML**: BeautifulSoup4 + html5lib parser

**Rationale**:
- pypdf is lightweight, pure Python, handles most standard PDFs (academic papers, books)
- pdfplumber offers better layout analysis for tables/complex formatting but is heavier
- ebooklib is the standard for EPUB parsing in Python ecosystem
- BeautifulSoup with html5lib is robust for messy HTML (handles malformed markup)

**Alternatives Considered**:
- PyMuPDF (fitz): Faster, more accurate, but requires external C library (harder deployment)
- pdfminer.six: Too low-level, requires significant boilerplate
- Unstructured library: Too heavyweight for MVP (37+ dependencies)

**Implementation Pattern**:
```python
def parse_pdf(file_path: str) -> str:
    try:
        return pypdf_extract(file_path)
    except (PDFSyntaxError, LayoutError):
        logger.warning("pypdf failed, falling back to pdfplumber")
        return pdfplumber_extract(file_path)
```

**References**:
- pypdf: https://pypdf.readthedocs.io/
- pdfplumber: https://github.com/jsvine/pdfplumber
- ebooklib: https://github.com/aerkalov/ebooklib

---

## 2. Text Chunking Strategy

### Decision: Fixed-size chunking with overlap (1000 tokens, 200 overlap)

**Rationale**:
- **Chunk Size (1000 tokens)**:
  - Balances retrieval precision (smaller = more precise) with context quality (larger = more context)
  - Fits well within GPT-4's context window after adding system prompt + history (~8k tokens)
  - Technical book content (explanations, code examples) benefits from larger chunks

- **Overlap (200 tokens, 20%)**:
  - Prevents concept fragmentation at chunk boundaries
  - Ensures critical information appearing near chunk edges is captured
  - Standard practice in RAG systems (10-20% overlap)

- **Token Counting**: Use tiktoken with cl100k_base encoding (GPT-4 tokenizer)

**Alternatives Considered**:
- 512 tokens (smaller): Too granular for technical explanations spanning multiple paragraphs
- Semantic chunking (sentence boundaries, paragraphs): More complex, minimal quality gain for book content
- LangChain RecursiveCharacterTextSplitter: Adds dependency, our custom impl is simpler

**Implementation Pattern**:
```python
import tiktoken

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    encoder = tiktoken.get_encoding("cl100k_base")
    tokens = encoder.encode(text)
    chunks = []

    for i in range(0, len(tokens), chunk_size - overlap):
        chunk_tokens = tokens[i:i + chunk_size]
        chunks.append(encoder.decode(chunk_tokens))

    return chunks
```

**References**:
- OpenAI tokenizer: https://github.com/openai/tiktoken
- RAG best practices: https://www.pinecone.io/learn/chunking-strategies/

---

## 3. Embedding Model Selection

### Decision: text-embedding-3-small (1536 dimensions)

**Rationale**:
- **Cost-Effective**: $0.02 per 1M tokens (vs $0.13 for text-embedding-3-large)
- **Sufficient Quality**: Outperforms ada-002 on MTEB benchmarks
- **Dimensionality**: 1536 dims balances storage/compute with retrieval quality
- **Hackathon Budget**: ~500 pages × 2000 tokens/page × $0.02/1M = $0.02 per book ingestion

**Alternatives Considered**:
- text-embedding-3-large (3072 dims): 2x cost, marginal quality improvement (not justified for MVP)
- text-embedding-ada-002: Older model, lower quality than 3-small
- Open-source (sentence-transformers): Requires GPU, adds hosting complexity

**Performance Comparison** (MTEB Average):
- text-embedding-3-small: 62.3%
- text-embedding-3-large: 64.6% (+2.3% for 6.5x cost)
- text-embedding-ada-002: 61.0%

**References**:
- OpenAI embeddings: https://platform.openai.com/docs/guides/embeddings
- MTEB benchmarks: https://huggingface.co/spaces/mteb/leaderboard

---

## 4. RAG Orchestration Pattern

### Decision: Stateful conversation with DB-persisted history

**Rationale**:
- **Conversation Quality**: Multi-turn context improves answer relevance (e.g., "What else?" refers to previous response)
- **Token Efficiency**: Store history in DB, load only last N turns (default: 5), prune older messages
- **User Experience**: Support session resumption (return later, continue conversation)
- **Debugging**: Persistent history enables conversation replay, quality analysis

**Alternatives Considered**:
- Stateless (pass full history in request): Simple but poor UX (client must manage history)
- In-memory session store: Lost on server restart, doesn't scale horizontally

**Context Window Management**:
1. Retrieve last 5 messages from DB (user + assistant pairs)
2. Build prompt: system + retrieved_chunks + history + new_query
3. Prune history if total exceeds 6000 tokens (keep system + retrieved_chunks + latest turn)

**Implementation Pattern**:
```python
async def build_prompt(session_id: UUID, query: str, retrieved_chunks: List[str]) -> List[Message]:
    history = await db.get_recent_messages(session_id, limit=5)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{'\n'.join(retrieved_chunks)}\n\nQuestion: {query}"}
    ]

    # Insert history before latest query
    for msg in history:
        messages.insert(-1, {"role": msg.role, "content": msg.content})

    return messages
```

**References**:
- Conversational RAG patterns: https://docs.anthropic.com/en/docs/build-with-claude/rag

---

## 5. Qdrant Collection Design

### Decision: Single collection with metadata filtering

**Collection Schema**:
```python
{
    "collection_name": "physical_ai_book_chunks",
    "vectors": {
        "size": 1536,  # text-embedding-3-small
        "distance": "Cosine"
    },
    "payload_schema": {
        "book_id": "keyword",      # Filter by book (future multi-book support)
        "chunk_id": "keyword",     # UUID reference
        "chunk_index": "integer",  # Position in book (for ordering)
        "text": "text",            # Original chunk text
        "metadata": {
            "page_number": "integer",
            "chapter": "text",
            "section": "text"
        }
    }
}
```

**Rationale**:
- **Single Collection**: Simpler ops, sufficient for MVP (1 book), easy to add book_id filter later
- **Cosine Distance**: Standard for semantic similarity (OpenAI embeddings are normalized)
- **Payload Indexing**: Index book_id as keyword for fast filtering (multi-book support)
- **Text in Payload**: Avoids separate DB lookup for retrieved chunks (trade-off: higher storage)

**Alternatives Considered**:
- Multiple collections (one per book): Over-engineered for MVP, harder to manage
- Euclidean distance: Cosine is standard for embeddings
- Store text in Postgres only: Requires join, higher latency

**Query Pattern**:
```python
results = qdrant_client.search(
    collection_name="physical_ai_book_chunks",
    query_vector=query_embedding,
    query_filter=models.Filter(
        must=[models.FieldCondition(key="book_id", match=models.MatchValue(value=book_id))]
    ),
    limit=5,
    with_payload=True
)
```

**References**:
- Qdrant collections: https://qdrant.tech/documentation/concepts/collections/
- Distance metrics: https://qdrant.tech/documentation/concepts/search/#metrics

---

## 6. Agent Framework Choice

### Decision: Custom agent loop (no framework)

**Rationale**:
- **Simplicity**: RAG flow is straightforward (embed → search → prompt → generate), no need for framework overhead
- **Cost**: OpenAI Assistants API charges markup; custom loop uses base API pricing
- **Control**: Full control over prompts, retrieval count, context pruning
- **Latency**: Direct API calls, no framework abstraction layer
- **Hackathon Timeline**: Faster to implement simple loop than learn framework

**Alternatives Considered**:
- **OpenAI Assistants API**: Easy but expensive, opaque (can't see exact prompts), file uploads stored by OpenAI (privacy concern)
- **ChatKit SDK**: Unclear documentation, adds dependency, minimal value over raw OpenAI SDK
- **LangChain**: Heavyweight (100+ deps), abstractions slow down iteration, overkill for RAG

**Custom Agent Loop** (simplified):
```python
async def chat(query: str, book_id: UUID, session_id: UUID | None) -> ChatResponse:
    # 1. Embed query
    query_embedding = await openai.embed(query)

    # 2. Retrieve chunks
    chunks = await qdrant.search(query_embedding, book_id=book_id, limit=5)

    # 3. Load history
    history = await db.get_messages(session_id) if session_id else []

    # 4. Build prompt
    messages = build_prompt(query, chunks, history)

    # 5. Generate response
    response = await openai.chat(messages, model="gpt-4o-mini", stream=True)

    # 6. Save to DB
    await db.save_messages(session_id, query, response)

    return ChatResponse(session_id=session_id, response=response, sources=chunks)
```

**References**:
- OpenAI Chat API: https://platform.openai.com/docs/guides/chat
- RAG from scratch: https://github.com/anthropics/anthropic-cookbook/blob/main/skills/retrieval_augmented_generation/guide.ipynb

---

## 7. Database Schema Design

### Decision: Normalized schema with JSONB for flexibility

**Postgres Schema**:

```sql
-- Books table
CREATE TABLE books (
    book_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    author TEXT,
    source_file_name TEXT NOT NULL,
    total_chunks INTEGER NOT NULL,
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB  -- Flexible: { isbn, publisher, version, etc. }
);

-- Book chunks metadata (embeddings in Qdrant)
CREATE TABLE book_chunks (
    chunk_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id UUID REFERENCES books(book_id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    text TEXT NOT NULL,  -- Duplicate in Qdrant, but useful for DB queries
    metadata JSONB,  -- { page_number, chapter, section }
    UNIQUE(book_id, chunk_index)
);
CREATE INDEX idx_chunks_book ON book_chunks(book_id);

-- Chat sessions
CREATE TABLE chat_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    book_id UUID REFERENCES books(book_id) ON DELETE CASCADE,
    mode TEXT CHECK (mode IN ('normal', 'selection')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB  -- { user_agent, ip, tags }
);
CREATE INDEX idx_sessions_book ON chat_sessions(book_id);

-- Messages
CREATE TABLE messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES chat_sessions(session_id) ON DELETE CASCADE,
    role TEXT CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB  -- { retrieved_chunks: [{chunk_id, score}], model, tokens }
);
CREATE INDEX idx_messages_session ON messages(session_id, timestamp);
```

**Rationale**:
- **Normalization**: Separate tables for logical entities (books, sessions, messages) - easier to query
- **JSONB Flexibility**: Schema evolution without migrations (e.g., add new book metadata fields)
- **Cascading Deletes**: Clean up dependent data automatically
- **Indexes**: Fast lookups by book_id, session_id
- **Text Duplication**: Store chunk text in both Postgres and Qdrant (trade-off: storage vs query simplicity)

**Alternatives Considered**:
- Denormalized (all in messages table): Harder to query, data duplication
- NoSQL (MongoDB): Unnecessary complexity, Postgres JSONB offers same flexibility

**References**:
- Postgres JSONB: https://www.postgresql.org/docs/current/datatype-json.html
- Neon Serverless: https://neon.tech/docs/introduction

---

## 8. Clarifications Resolved

### 8.1 Selected-text Q&A Conversation History

**Question**: Does selected-text Q&A need conversation history, or is it stateless?

**Decision**: Support multi-turn for both modes (store in DB)

**Rationale**:
- Users may ask follow-up questions about selected text ("What does this mean?", "Explain more")
- Consistent UX: Both modes support conversation continuity
- Implementation cost is minimal (same DB schema, just skip vector search)

---

### 8.2 Book Ingestion Idempotency

**Question**: Should `/ingest/book` be idempotent? (re-uploading same book)

**Decision**: Yes, use book_id as unique key, allow re-ingestion

**Implementation**:
- If book_id provided in request and exists in DB: delete old chunks, re-ingest (UPDATE flow)
- If no book_id or new ID: create new book entry (INSERT flow)
- Qdrant: delete by book_id filter, then upsert new chunks
- Use case: Update book with new edition, fix parsing errors

**Rationale**: Simplifies iteration during development, supports future "re-index" feature

---

### 8.3 Chat Response Streaming

**Question**: Real-time streaming for chat responses or return full response?

**Decision**: Implement streaming via Server-Sent Events (SSE)

**Rationale**:
- **UX**: Real-time typing effect, lower perceived latency (LLM responses can take 3-5 seconds)
- **Standard**: SSE is standard for chat applications (ChatGPT, Claude, etc.)
- **OpenAI Support**: Chat completions API supports streaming natively
- **Incremental Rendering**: Frontend can display response as it generates

**Implementation Pattern**:
```python
from fastapi.responses import StreamingResponse

async def stream_chat_response(messages: List[Message]):
    async for chunk in openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    ):
        if chunk.choices[0].delta.content:
            yield f"data: {chunk.choices[0].delta.content}\n\n"

    yield "data: [DONE]\n\n"

@router.post("/chat")
async def chat(request: ChatRequest):
    # ... (embed, retrieve, build prompt)
    return StreamingResponse(stream_chat_response(messages), media_type="text/event-stream")
```

**Alternatives Considered**:
- Polling: Poor UX, higher server load
- WebSockets: Bi-directional unnecessary (chat is one-way streaming), more complex
- Full response: Simple but poor UX for long responses

**References**:
- OpenAI streaming: https://platform.openai.com/docs/api-reference/streaming
- SSE spec: https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events

---

## Technology Stack Summary

| Component | Technology | Version | Rationale |
|-----------|-----------|---------|-----------|
| **Web Framework** | FastAPI | 0.104+ | Async support, auto OpenAPI docs, Pydantic validation |
| **LLM API** | OpenAI SDK | 1.3+ | GPT-4o-mini for chat, text-embedding-3-small for embeddings |
| **Vector DB** | Qdrant Cloud | 1.7+ | Cloud-native, superior search performance, easy scaling |
| **Relational DB** | Neon Serverless Postgres | psycopg 3.1+ | Serverless (auto-scaling), JSONB for flexibility |
| **PDF Parser** | pypdf + pdfplumber | 3.17+ | Lightweight primary + robust fallback |
| **EPUB Parser** | ebooklib | 0.18+ | Standard Python EPUB library |
| **HTML Parser** | BeautifulSoup4 | 4.12+ | Robust, handles malformed HTML |
| **Tokenizer** | tiktoken | Latest | Official OpenAI tokenizer (cl100k_base) |
| **Testing** | pytest + httpx | 7.4+ | Async test support, FastAPI integration |
| **Logging** | loguru | Latest | Structured logging, better than stdlib logging |
| **Server** | uvicorn | 0.24+ | ASGI server for FastAPI |

---

## Open Questions for Future Iterations

1. **Authentication**: Add user accounts and API key auth?
2. **Multi-book Support**: How to handle book discovery/search across multiple books?
3. **Conversation Export**: Allow users to export chat history as PDF/Markdown?
4. **Quality Metrics**: Track retrieval quality (relevance scores, user feedback)?
5. **Caching**: Cache embeddings for common queries to reduce OpenAI costs?

---

**Status**: Research complete, ready for Phase 1 design artifacts
**Next**: Generate `data-model.md`, `contracts/api.openapi.yaml`, `quickstart.md`
