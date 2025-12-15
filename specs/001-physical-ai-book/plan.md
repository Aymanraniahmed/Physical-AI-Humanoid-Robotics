# Implementation Plan: RAG Chatbot Backend for AI-Native Book Platform

**Branch**: `001-physical-ai-book` | **Date**: 2025-12-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-physical-ai-book/spec.md` + user request for RAG chatbot backend

## Summary

Build a production-ready RAG (Retrieval-Augmented Generation) chatbot backend for an AI-native book platform that supports both full-book semantic search and selected-text Q&A. The system uses FastAPI for the backend API, Neon Serverless Postgres for metadata and chat history, Qdrant Cloud for vector search, and OpenAI Agents/ChatKit SDK for multi-turn reasoning. The backend provides three core APIs: `/ingest/book` for processing and embedding book content (PDF/HTML/EPUB), `/chat` for normal RAG question-answering with vector search, and `/chat/selection` for selected-text Q&A that bypasses vector search and operates only on user-provided text.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**:
- FastAPI 0.104+ (async web framework)
- OpenAI SDK 1.3+ (GPT-4 agents, embeddings)
- Qdrant Client 1.7+ (vector database)
- psycopg[binary] 3.1+ (Neon Postgres async driver)
- pypdf 3.17+, ebooklib 0.18+, beautifulsoup4 4.12+ (document parsing)
- python-multipart (file upload support)
- pydantic 2.5+ (data validation)
- uvicorn 0.24+ (ASGI server)

**Storage**:
- Neon Serverless Postgres (user metadata, chat sessions, conversation history)
- Qdrant Cloud (vector embeddings for book chunks, semantic search)

**Testing**: pytest 7.4+, pytest-asyncio, httpx (async test client)

**Target Platform**: Linux server (Docker container, deployable to Render/Railway/Fly.io)

**Project Type**: Single backend API service (web)

**Performance Goals**:
- Ingest API: Process 100-page PDF in <60 seconds
- Chat API: <2s p95 latency for RAG queries (embed + search + LLM)
- Selection API: <1s p95 latency (LLM-only, no vector search)
- Support 100 concurrent users

**Constraints**:
- Selected-text Q&A MUST NOT call Qdrant (architecture constraint)
- All API keys (OpenAI, Qdrant, Neon) via environment variables
- Hackathon-ready: modular, documented, production-oriented
- Support streaming responses for real-time chat UX

**Scale/Scope**:
- MVP: Single book (Physical AI Humanoid Robotics)
- 500-1000 chunks per book (~500-1000 pages)
- 1000+ chat sessions
- Multi-turn conversations (5-10 turns average)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Note**: The constitution.md is currently a template. Applying general best practices for this hackathon project:

✅ **Modularity**: Backend organized into clear modules (ingest, chat, models, database)
✅ **Testability**: pytest-based unit tests for services, integration tests for APIs
✅ **CLI Support**: No CLI required for MVP (API-first); can add admin CLI later
✅ **Observability**: Structured logging (loguru), request IDs, error tracking
✅ **Security**: Environment variables for secrets, input validation via Pydantic
✅ **Simplicity**: Start with monolithic FastAPI app; no premature microservices

**Re-evaluation Required**: After Phase 1 design artifacts complete

## Project Structure

### Documentation (this feature)

```text
specs/001-physical-ai-book/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technology decisions, patterns)
├── data-model.md        # Phase 1 output (entities, schemas, relationships)
├── quickstart.md        # Phase 1 output (setup, run, test instructions)
├── contracts/           # Phase 1 output (OpenAPI specs)
│   └── api.openapi.yaml # Full API contract
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Environment variables, settings (Pydantic Settings)
│   ├── models/                 # Data models
│   │   ├── book.py             # Book, BookChunk schemas
│   │   ├── chat.py             # ChatSession, Message, ChatRequest/Response
│   │   └── user.py             # User metadata (optional for MVP)
│   ├── services/               # Business logic
│   │   ├── ingest.py           # Document parsing, chunking, embedding
│   │   ├── vector_store.py     # Qdrant operations (upsert, search)
│   │   ├── chat_service.py     # RAG orchestration (normal Q&A)
│   │   ├── selection_service.py # Selected-text Q&A (no vector search)
│   │   └── database.py         # Neon Postgres operations (async)
│   ├── routers/                # API route handlers
│   │   ├── ingest.py           # POST /ingest/book
│   │   ├── chat.py             # POST /chat, POST /chat/selection
│   │   └── health.py           # GET /health (readiness probe)
│   └── utils/                  # Helpers
│       ├── chunking.py         # Text chunking strategies
│       ├── parsers.py          # PDF/HTML/EPUB parsers
│       └── logging.py          # Structured logging setup
├── tests/
│   ├── unit/
│   │   ├── test_chunking.py
│   │   ├── test_parsers.py
│   │   └── test_services.py
│   ├── integration/
│   │   ├── test_ingest_api.py
│   │   ├── test_chat_api.py
│   │   └── test_database.py
│   └── fixtures/
│       └── sample.pdf          # Test document
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container image
└── README.md                   # Setup instructions

frontend/
├── (existing Next.js app)
└── (integrate with backend APIs)
```

**Structure Decision**: Monolithic backend service (`backend/`) with modular internal structure. Separates routing, business logic (services), data models, and database operations. Uses FastAPI's dependency injection for database connections and config. Frontend already exists; backend will be consumed via API calls.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

N/A - No constitutional violations detected. Architecture follows simplicity principles: single backend service, clear separation of concerns, no premature abstractions.

---

## Phase 0: Research & Technology Decisions

**Output**: `research.md`

### Research Tasks

1. **Document Parsing Strategy**
   - Question: Best approach for extracting text from PDF/HTML/EPUB while preserving structure?
   - Research: pypdf vs pdfplumber vs PyMuPDF; ebooklib for EPUB; BeautifulSoup for HTML
   - Decision criteria: Accuracy, metadata extraction, layout preservation

2. **Text Chunking Strategy**
   - Question: How to chunk book content for optimal retrieval?
   - Research: Fixed-size vs semantic chunking, chunk size (512 vs 1024 tokens), overlap strategies
   - Decision criteria: Retrieval quality, embedding cost, context window utilization

3. **Embedding Model Selection**
   - Question: Which OpenAI embedding model? text-embedding-3-small vs text-embedding-3-large
   - Research: Cost, dimensionality, retrieval quality benchmarks
   - Decision criteria: Performance vs cost trade-off for hackathon

4. **RAG Orchestration Pattern**
   - Question: How to structure multi-turn conversation with context?
   - Research: Stateless (pass full history) vs stateful (store in DB), context pruning strategies
   - Decision criteria: Latency, token costs, conversation coherence

5. **Qdrant Collection Design**
   - Question: Single collection or multiple? Metadata filtering approach?
   - Research: Qdrant payload structure, filtering performance, multi-tenancy patterns
   - Decision criteria: Query flexibility, scalability

6. **Agent Framework Choice**
   - Question: OpenAI Assistants API vs ChatKit SDK vs custom agent loop?
   - Research: Feature comparison, cost, control over prompts
   - Decision criteria: Hackathon timeline, extensibility

7. **Database Schema Design**
   - Question: How to model chat sessions, messages, and book metadata in Postgres?
   - Research: Normalization vs denormalization, JSON columns for flexibility
   - Decision criteria: Query patterns, future extensibility

### Unknowns to Resolve

- **NEEDS CLARIFICATION**: Does selected-text Q&A need conversation history, or is it stateless?
  - Assumption for research: Support multi-turn for both modes (store in DB)

- **NEEDS CLARIFICATION**: Should `/ingest/book` be idempotent? (re-uploading same book)
  - Assumption for research: Yes, use book_id as unique key, allow re-ingestion

- **NEEDS CLARIFICATION**: Real-time streaming for chat responses or return full response?
  - Assumption for research: Implement streaming via Server-Sent Events (SSE) for better UX

---

## Phase 1: Design Artifacts

**Outputs**: `data-model.md`, `contracts/api.openapi.yaml`, `quickstart.md`

### 1. Data Model Design (`data-model.md`)

**Entities**:

- **Book**: Unique book metadata
  - Fields: `book_id` (UUID), `title`, `author`, `source_file_name`, `total_chunks`, `ingested_at`, `metadata` (JSONB)

- **BookChunk**: Vector-indexed text segments
  - Fields: `chunk_id` (UUID), `book_id` (FK), `chunk_index` (int), `text` (TEXT), `embedding` (stored in Qdrant), `metadata` (JSONB: page_number, chapter, etc.)
  - Stored: Metadata in Postgres, embeddings + text in Qdrant

- **ChatSession**: Conversation context
  - Fields: `session_id` (UUID), `book_id` (FK), `mode` (enum: 'normal' | 'selection'), `created_at`, `updated_at`, `metadata` (JSONB)

- **Message**: Individual chat turns
  - Fields: `message_id` (UUID), `session_id` (FK), `role` (enum: 'user' | 'assistant'), `content` (TEXT), `timestamp`, `metadata` (JSONB: retrieved_chunks for 'normal' mode)

**Relationships**:
- Book 1→N BookChunk (metadata only in Postgres)
- Book 1→N ChatSession
- ChatSession 1→N Message

**State Transitions**:
- ChatSession: created → active (messages added) → archived (optional)

### 2. API Contracts (`contracts/api.openapi.yaml`)

**Endpoints**:

**POST /ingest/book**
- Request: `multipart/form-data` with `file` (PDF/HTML/EPUB), optional `book_id`, `metadata`
- Response: `{ "book_id": "uuid", "title": "string", "total_chunks": 123, "status": "completed" }`
- Flow: Parse document → chunk text → generate embeddings → upsert to Qdrant → save metadata to Postgres

**POST /chat**
- Request: `{ "session_id": "uuid?", "book_id": "uuid", "message": "string" }`
- Response: `{ "session_id": "uuid", "response": "string", "sources": [{"chunk_id": "uuid", "text": "...", "score": 0.95}] }`
- Flow: Embed query → search Qdrant → retrieve top-k chunks → build prompt with context + history → call OpenAI → save message to DB → return response

**POST /chat/selection**
- Request: `{ "session_id": "uuid?", "selected_text": "string", "question": "string" }`
- Response: `{ "session_id": "uuid", "response": "string" }`
- Flow: Build prompt with selected_text + question + history → call OpenAI (NO Qdrant) → save message to DB → return response
- Constraint: MUST NOT call Qdrant; operates only on `selected_text`

**GET /health**
- Response: `{ "status": "healthy", "services": { "postgres": "up", "qdrant": "up", "openai": "up" } }`

### 3. Quickstart Guide (`quickstart.md`)

**Prerequisites**: Python 3.11+, Docker (optional), API keys (OpenAI, Qdrant Cloud, Neon)

**Setup Steps**:
1. Clone repository
2. Copy `.env.example` to `.env`, fill in API keys
3. Install dependencies: `pip install -r backend/requirements.txt`
4. Run migrations (if using Alembic): `alembic upgrade head`
5. Start server: `uvicorn app.main:app --reload`
6. Test health: `curl http://localhost:8000/health`
7. Ingest book: `curl -X POST -F "file=@book.pdf" http://localhost:8000/ingest/book`
8. Chat: `curl -X POST -H "Content-Type: application/json" -d '{"book_id": "uuid", "message": "What is Physical AI?"}' http://localhost:8000/chat`

---

## Phase 2: Implementation Tasks

**Output**: `tasks.md` (generated by `/sp.tasks`, NOT by this `/sp.plan` command)

This phase breaks down the architecture into executable, testable tasks. Run `/sp.tasks` after this plan is approved.

**Expected task categories**:
1. Project scaffolding (FastAPI app, config, folder structure)
2. Database setup (Neon connection, schema, migrations)
3. Document parsers (PDF, HTML, EPUB)
4. Chunking service (text splitting, overlap)
5. Embedding & vector store (OpenAI embeddings, Qdrant upsert/search)
6. Ingest API endpoint (upload, parse, chunk, embed)
7. Chat service (RAG orchestration, prompt engineering)
8. Selection service (text-only Q&A, no vector search)
9. Chat API endpoints (/chat, /chat/selection)
10. Database operations (save sessions, messages)
11. Health check endpoint
12. Testing (unit, integration, fixtures)
13. Documentation (README, .env.example, API docs)
14. Deployment (Dockerfile, environment setup)

---

## Data Flow Diagrams

### Flow 1: Book Ingestion (`/ingest/book`)

```
User → POST /ingest/book (file upload)
  ↓
FastAPI Router (app/routers/ingest.py)
  ↓
IngestService (app/services/ingest.py)
  ├→ Parse document (parsers.py: PDF/HTML/EPUB → raw text)
  ├→ Chunk text (chunking.py: text → chunks with overlap)
  ├→ Generate embeddings (OpenAI API: chunks → vectors)
  ├→ Upsert to Qdrant (vector_store.py: store embeddings + metadata)
  └→ Save book metadata to Postgres (database.py: book + chunk metadata)
  ↓
Response: { book_id, title, total_chunks, status }
```

### Flow 2: Normal RAG Chat (`/chat`)

```
User → POST /chat { session_id?, book_id, message }
  ↓
FastAPI Router (app/routers/chat.py)
  ↓
ChatService (app/services/chat_service.py)
  ├→ Load session history from Postgres (if session_id provided)
  ├→ Embed user query (OpenAI Embeddings API)
  ├→ Vector search in Qdrant (top-k relevant chunks)
  ├→ Build prompt:
  │    - System: "You are a helpful assistant for the Physical AI book"
  │    - Context: Retrieved chunks
  │    - History: Previous messages
  │    - User: Current question
  ├→ Call OpenAI Chat API (GPT-4 with streaming)
  ├→ Save user message + assistant response to Postgres
  └→ Return response with sources
  ↓
Response: { session_id, response, sources: [{chunk_id, text, score}] }
```

### Flow 3: Selected-Text Chat (`/chat/selection`)

```
User → POST /chat/selection { session_id?, selected_text, question }
  ↓
FastAPI Router (app/routers/chat.py)
  ↓
SelectionService (app/services/selection_service.py)
  ├→ Load session history from Postgres (if session_id provided)
  ├→ Build prompt:
  │    - System: "Answer based ONLY on the provided text"
  │    - Context: selected_text (NO Qdrant search)
  │    - History: Previous messages
  │    - User: question
  ├→ Call OpenAI Chat API (GPT-4 with streaming)
  ├→ Save user message + assistant response to Postgres
  └→ Return response
  ↓
Response: { session_id, response }

CONSTRAINT: SelectionService NEVER calls VectorStore/Qdrant
```

---

## Key Design Decisions

### 1. Embedding Model: text-embedding-3-small
**Rationale**: Cost-effective for hackathon, 1536 dimensions, sufficient retrieval quality for book-length content.
**Alternative**: text-embedding-3-large (3072 dims) - rejected due to 2x cost, marginal quality improvement.

### 2. Chunk Size: 1000 tokens, 200 token overlap
**Rationale**: Balances context (enough for paragraph-level semantics) and retrieval precision. Overlap ensures concepts spanning chunk boundaries are captured.
**Alternative**: 512 tokens - rejected as too small for technical book content with complex explanations.

### 3. Database: Postgres for metadata + chat history, Qdrant for vectors
**Rationale**: Separation of concerns. Postgres handles structured data (sessions, messages, book metadata); Qdrant optimized for vector search. Avoids pgvector extension complexity.
**Alternative**: pgvector (all in Postgres) - rejected due to Qdrant's superior vector search performance and cloud-native scaling.

### 4. Agent Framework: Custom agent loop (not OpenAI Assistants API)
**Rationale**: Full control over prompts, cheaper (Assistants API has markup), faster iteration for hackathon.
**Alternative**: OpenAI Assistants API - rejected due to cost and opacity; ChatKit SDK - evaluated but custom loop simpler for MVP.

### 5. Selected-text architecture: Separate service class
**Rationale**: Enforces constraint (no Qdrant calls) at code level. Clear separation prevents accidental vector search in selection mode.
**Alternative**: Single service with mode flag - rejected as too error-prone.

### 6. Streaming: Server-Sent Events (SSE)
**Rationale**: Real-time UX, lower perceived latency for long responses, standard for chat applications.
**Alternative**: Polling - rejected due to poor UX; WebSockets - overkill for one-way streaming.

---

## Non-Functional Requirements

### Performance
- **Ingest**: <60s for 100-page PDF (embedding is bottleneck; batch requests)
- **Chat**: <2s p95 (embed: ~100ms, Qdrant: ~50ms, GPT-4: ~1.5s)
- **Selection**: <1s p95 (GPT-4 only, no vector search overhead)

### Reliability
- **Error Handling**: Retry logic for OpenAI (exponential backoff), Qdrant (connection pooling)
- **Graceful Degradation**: If Qdrant down, return error but don't crash; health check reports service status

### Security
- **API Keys**: Environment variables only, never hardcoded
- **Input Validation**: Pydantic models for all requests, file type validation (PDF/HTML/EPUB only)
- **Rate Limiting**: (Future) Add per-user rate limits to prevent abuse

### Observability
- **Logging**: Structured logs (JSON) with request IDs, service tags (loguru)
- **Metrics**: (Future) Prometheus metrics for latency, error rates
- **Tracing**: (Future) OpenTelemetry for distributed tracing

---

## Risk Analysis

### Risk 1: Qdrant Cloud Latency
**Impact**: High (affects all normal chat queries)
**Likelihood**: Medium (cloud service, network dependency)
**Mitigation**: Connection pooling, retry logic, timeout limits; fallback: warn user of degraded performance
**Kill Switch**: Disable normal chat, redirect to selection-only mode

### Risk 2: OpenAI API Cost Overruns
**Impact**: Medium (budget constraint for hackathon)
**Likelihood**: Medium (depends on usage)
**Mitigation**: Use cheaper model (gpt-4o-mini) for development; rate limiting; prompt optimization to reduce tokens
**Kill Switch**: Disable service if budget threshold exceeded

### Risk 3: Large Document Parsing Failures
**Impact**: Medium (blocks ingestion for some books)
**Likelihood**: Low (pypdf handles most PDFs)
**Mitigation**: Fallback parsers (pdfplumber, PyMuPDF), error logging, return partial results
**Kill Switch**: Manual upload of pre-processed text

---

## Evaluation & Validation

### Definition of Done
- [ ] All API endpoints functional (`/ingest/book`, `/chat`, `/chat/selection`, `/health`)
- [ ] Selected-text Q&A does NOT call Qdrant (code review + integration test)
- [ ] Ingest processes PDF/HTML/EPUB successfully (test with sample files)
- [ ] Normal chat retrieves relevant chunks from Qdrant (retrieval quality test)
- [ ] Multi-turn conversations maintain context (session history test)
- [ ] Unit tests cover parsing, chunking, embedding logic (>80% coverage)
- [ ] Integration tests cover end-to-end API flows
- [ ] `.env.example` template complete with all required keys
- [ ] README with quickstart instructions
- [ ] Deployed to staging environment (Render/Railway)

### Output Validation
- **Format**: OpenAPI spec validates all request/response schemas
- **Requirements**: All functional requirements from user input satisfied
- **Safety**: Input validation prevents injection attacks, file upload restricted to safe types

---

## Architectural Decision Records (ADR)

📋 **Architectural decision detected**: Database split (Postgres for metadata, Qdrant for vectors) vs unified pgvector approach
📋 **Architectural decision detected**: Custom agent loop vs OpenAI Assistants API for RAG orchestration
📋 **Architectural decision detected**: Separate SelectionService to enforce no-Qdrant constraint for selected-text Q&A

**Document reasoning and tradeoffs?** Run `/sp.adr <decision-title>` for each decision above.

---

## Next Steps

1. ✅ **Phase 0 Complete**: This plan document generated
2. **Phase 1 Next**: Generate `research.md`, `data-model.md`, `contracts/api.openapi.yaml`, `quickstart.md`
3. **Phase 2 After Approval**: Run `/sp.tasks` to break down into executable tasks
4. **Implementation**: Follow TDD workflow (write tests → implement → refactor)

---

**Plan Status**: Ready for review and Phase 1 artifact generation
**Branch**: `001-physical-ai-book`
**Estimated Effort**: 2-3 days for MVP (hackathon timeline)
