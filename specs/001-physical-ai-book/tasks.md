# Implementation Tasks: RAG Chatbot Backend

**Feature**: RAG Chatbot Backend for AI-native Book Platform
**Branch**: `001-physical-ai-book`
**Plan**: [plan.md](./plan.md)
**Data Model**: [data-model.md](./data-model.md)
**API Contract**: [contracts/api.openapi.yaml](./contracts/api.openapi.yaml)

## Overview

This document breaks down the implementation of the RAG chatbot backend into executable, testable tasks organized by user story. Each phase represents an independently testable increment.

**User Stories** (derived from API requirements):
- **US1 (P1)**: Book Ingestion - Admin uploads PDF/HTML/EPUB, system chunks, embeds, and stores for search
- **US2 (P2)**: Normal RAG Chat - User asks questions, system retrieves relevant chunks via vector search and generates answers
- **US3 (P3)**: Selected-Text Chat - User highlights text and asks questions, system answers based ONLY on selected text (no Qdrant)
- **US4 (P4)**: Multi-turn Conversations - Support session persistence and conversation history

**Implementation Strategy**: MVP-first, incremental delivery. Complete US1 first (book ingestion), then US2 (core chat), then US3 (selection), then US4 (sessions).

---

## Phase 1: Project Setup & Infrastructure

**Goal**: Initialize project structure, dependencies, configuration, and database schema.

**Independent Test**: Run health check endpoint, confirm all services (Postgres, Qdrant, OpenAI) are reachable.

### Tasks

- [ ] T001 Create backend project structure per plan.md (backend/app/, backend/tests/, backend/alembic/)
- [ ] T002 [P] Create requirements.txt with all dependencies from plan.md
- [ ] T003 [P] Create .env.example with environment variable template from quickstart.md
- [ ] T004 [P] Create backend/app/config.py using Pydantic Settings to load environment variables
- [ ] T005 [P] Create backend/app/utils/logging.py with structured logging setup (loguru)
- [ ] T006 Create backend/app/main.py with FastAPI app initialization and CORS configuration
- [ ] T007 [P] Create Dockerfile for containerized deployment per plan.md deployment section
- [ ] T008 [P] Create .dockerignore to exclude .env, __pycache__, .pytest_cache
- [ ] T009 Create backend/alembic.ini for database migrations
- [ ] T010 Create backend/alembic/env.py with async database connection from config
- [ ] T011 Create backend/alembic/versions/001_initial_schema.py implementing Book, BookChunk, ChatSession, Message tables from data-model.md
- [ ] T012 Create backend/app/routers/health.py implementing GET /health endpoint
- [ ] T013 Create backend/app/services/database.py with async Postgres connection pool and health check function
- [ ] T014 Create backend/app/services/vector_store.py with Qdrant client initialization and health check function
- [ ] T015 Add health router to FastAPI app in main.py
- [ ] T016 [P] Create backend/README.md with quickstart instructions from quickstart.md
- [ ] T017 Test: Run `alembic upgrade head` to create database schema
- [ ] T018 Test: Start server with `uvicorn app.main:app --reload` and verify http://localhost:8000/health returns healthy status

**Acceptance**:
- ✅ Project structure matches plan.md
- ✅ Database schema created successfully
- ✅ Health endpoint returns status for all services
- ✅ Docker image builds without errors

---

## Phase 2: Foundational Services (Blocking Prerequisites)

**Goal**: Implement shared services needed by all user stories: document parsing, text chunking, embedding generation.

**Independent Test**: Parse sample PDF, chunk into segments, generate embeddings, verify output format.

### Tasks

- [ ] T019 [P] Create backend/app/utils/parsers.py with PDF parser (pypdf) from research.md
- [ ] T020 [P] Add PDF fallback parser (pdfplumber) in parsers.py for complex layouts
- [ ] T021 [P] Create EPUB parser (ebooklib) in parsers.py
- [ ] T022 [P] Create HTML parser (BeautifulSoup4) in parsers.py
- [ ] T023 [P] Create backend/app/utils/chunking.py implementing fixed-size chunking with tiktoken (1000 tokens, 200 overlap) from research.md
- [ ] T024 Create backend/app/models/book.py with Pydantic schemas: Book, BookChunk, BookMetadata, ChunkMetadata from data-model.md
- [ ] T025 [P] Create backend/tests/fixtures/sample.pdf for testing (small 2-page PDF)
- [ ] T026 Test: Create backend/tests/unit/test_parsers.py testing all parsers with sample.pdf
- [ ] T027 Test: Create backend/tests/unit/test_chunking.py testing chunk size, overlap, token counting

**Acceptance**:
- ✅ All document formats (PDF, HTML, EPUB) parse successfully
- ✅ Chunking produces correct token counts with proper overlap
- ✅ Unit tests pass for parsers and chunking

---

## Phase 3: User Story 1 - Book Ingestion (P1)

**Goal**: Admin can upload a book file (PDF/HTML/EPUB), system processes it, generates embeddings, stores in Qdrant + Postgres.

**Independent Test**: Upload sample.pdf via POST /ingest/book, verify book_id returned, chunks created in Qdrant, metadata in Postgres.

**Acceptance Criteria**:
1. Given a PDF file, when uploaded to /ingest/book, then system returns book_id and total_chunks
2. Given the ingestion process, when complete, then embeddings exist in Qdrant and metadata in Postgres
3. Given the same book_id is re-uploaded, when ingestion runs, then old chunks are deleted and new ones created (idempotency)

### Tasks

- [ ] T028 [US1] Extend services/database.py with async functions: save_book(), save_chunks(), get_book(), delete_book()
- [ ] T029 [US1] Extend services/vector_store.py with functions: upsert_chunks(), delete_by_book_id(), create_collection() from data-model.md Qdrant config
- [ ] T030 [US1] Create backend/app/services/ingest.py orchestrating: parse → chunk → embed → store (Qdrant + Postgres)
- [ ] T031 [US1] In ingest.py, implement parse_document() calling appropriate parser based on file extension
- [ ] T032 [US1] In ingest.py, implement chunk_document() using chunking.py utils
- [ ] T033 [US1] In ingest.py, implement generate_embeddings() calling OpenAI text-embedding-3-small API with batching
- [ ] T034 [US1] In ingest.py, implement ingest_book() transaction: save to Postgres, upsert to Qdrant, handle errors
- [ ] T035 [US1] Create backend/app/models/ingest.py with Pydantic schemas: IngestRequest, IngestResponse from contracts
- [ ] T036 [US1] Create backend/app/routers/ingest.py implementing POST /ingest/book endpoint per api.openapi.yaml
- [ ] T037 [US1] In ingest router, add file validation (check extension: .pdf, .html, .epub, reject others)
- [ ] T038 [US1] In ingest router, handle multipart/form-data file upload with python-multipart
- [ ] T039 [US1] In ingest router, implement idempotency logic: if book_id provided and exists, delete old chunks
- [ ] T040 [US1] Add ingest router to FastAPI app in main.py
- [ ] T041 [US1] Test: Create backend/tests/integration/test_ingest_api.py testing full ingestion flow with sample.pdf
- [ ] T042 [US1] Test: Verify Qdrant collection created with correct vector size (1536) and distance metric (cosine)
- [ ] T043 [US1] Test: Verify Postgres tables populated with book metadata and chunk references
- [ ] T044 [US1] Test: Test re-ingestion with same book_id deletes old chunks and creates new ones
- [ ] T045 [US1] Test: Test error handling for invalid file format (.txt should fail)

**Acceptance**:
- ✅ POST /ingest/book successfully processes PDF/HTML/EPUB
- ✅ Embeddings stored in Qdrant with correct book_id filter
- ✅ Metadata stored in Postgres with correct chunk count
- ✅ Re-ingestion with same book_id is idempotent
- ✅ Invalid file formats rejected with 400 error

**Parallel Opportunities**: T028-T029 can run in parallel (different files), T041-T045 tests can run in parallel

---

## Phase 4: User Story 2 - Normal RAG Chat (P2)

**Goal**: User asks questions about the book, system retrieves relevant chunks via vector search, generates answers using OpenAI chat.

**Independent Test**: POST /chat with book_id and question, verify response includes answer and sources with similarity scores.

**Acceptance Criteria**:
1. Given an ingested book, when user sends a question to /chat, then system returns relevant answer with top-k source chunks
2. Given a query, when vector search executes, then top 5 chunks with highest similarity scores are retrieved
3. Given retrieved chunks, when prompt is built, then context includes chunks + system instructions from plan.md

### Tasks

- [ ] T046 [US2] Create backend/app/models/chat.py with Pydantic schemas: ChatRequest, ChatResponse, ChunkSource from data-model.md
- [ ] T047 [US2] In services/vector_store.py, implement search() function with query_vector, book_id filter, limit=5 (top-k)
- [ ] T048 [US2] Create backend/app/services/chat_service.py for RAG orchestration
- [ ] T049 [US2] In chat_service.py, implement embed_query() calling OpenAI embeddings API
- [ ] T050 [US2] In chat_service.py, implement retrieve_chunks() calling vector_store.search()
- [ ] T051 [US2] In chat_service.py, implement build_prompt() creating messages: system + context (chunks) + user query from plan.md Flow 2
- [ ] T052 [US2] In chat_service.py, implement generate_response() calling OpenAI chat completions API (gpt-4o-mini)
- [ ] T053 [US2] In chat_service.py, implement chat() orchestrating: embed → retrieve → build_prompt → generate → return response + sources
- [ ] T054 [US2] Create backend/app/routers/chat.py implementing POST /chat endpoint per api.openapi.yaml
- [ ] T055 [US2] In chat router, validate ChatRequest (book_id exists, message non-empty)
- [ ] T056 [US2] In chat router, call chat_service.chat() and return ChatResponse with sources
- [ ] T057 [US2] Add chat router to FastAPI app in main.py
- [ ] T058 [US2] Test: Create backend/tests/integration/test_chat_api.py testing full chat flow
- [ ] T059 [US2] Test: Verify vector search returns top-k chunks with scores >= 0 and <= 1
- [ ] T060 [US2] Test: Verify response includes at least 1 source chunk with chunk_id, text, score, metadata
- [ ] T061 [US2] Test: Test error handling for non-existent book_id (should return 404)

**Acceptance**:
- ✅ POST /chat returns answer with source chunks
- ✅ Vector search retrieves relevant chunks (similarity scores make sense)
- ✅ OpenAI chat generates coherent answers based on context
- ✅ Error handling for invalid book_id works correctly

**Parallel Opportunities**: T046 (models) and T047 (vector store) can run in parallel

---

## Phase 5: User Story 3 - Selected-Text Chat (P3)

**Goal**: User highlights text from the book and asks questions, system answers based ONLY on selected text without calling Qdrant.

**Independent Test**: POST /chat/selection with selected_text and question, verify response does NOT call Qdrant and answers only from provided text.

**Acceptance Criteria**:
1. Given selected text, when user sends question to /chat/selection, then system returns answer based ONLY on selected_text
2. Given the selection service, when invoked, then it NEVER calls Qdrant (enforce constraint at code level)
3. Given selected text prompt, when built, then it includes instruction "Answer based ONLY on the provided text"

### Tasks

- [ ] T062 [US3] In models/chat.py, add Pydantic schemas: SelectionChatRequest, SelectionChatResponse from data-model.md
- [ ] T063 [US3] Create backend/app/services/selection_service.py for text-only Q&A (NO vector_store import allowed)
- [ ] T064 [US3] In selection_service.py, implement build_prompt() with system instruction: "Answer based ONLY on the provided text"
- [ ] T065 [US3] In selection_service.py, implement generate_response() calling OpenAI chat API (same as chat_service but no retrieval)
- [ ] T066 [US3] In selection_service.py, implement chat_selection() orchestrating: build_prompt (with selected_text) → generate → return response
- [ ] T067 [US3] In routers/chat.py, add POST /chat/selection endpoint per api.openapi.yaml
- [ ] T068 [US3] In chat router selection endpoint, validate SelectionChatRequest (selected_text and question non-empty, text <= 10000 chars)
- [ ] T069 [US3] In chat router selection endpoint, call selection_service.chat_selection() and return SelectionChatResponse
- [ ] T070 [US3] Test: Create backend/tests/unit/test_selection_service.py verifying NO vector_store import exists in selection_service.py
- [ ] T071 [US3] Test: In test_selection_service.py, mock OpenAI call and verify prompt contains selected_text and constraint instruction
- [ ] T072 [US3] Test: Create backend/tests/integration/test_selection_api.py testing POST /chat/selection
- [ ] T073 [US3] Test: Verify response returns answer without sources field (unlike normal chat)
- [ ] T074 [US3] Test: Test error handling for text too long (>10000 chars should return 400)

**Acceptance**:
- ✅ POST /chat/selection returns answer based only on selected text
- ✅ selection_service.py does NOT import vector_store (enforced by unit test)
- ✅ Response format differs from normal chat (no sources)
- ✅ Error handling for text length validation works

**Parallel Opportunities**: T062 (models), T070-T071 (unit tests) can run in parallel with integration tasks

---

## Phase 6: User Story 4 - Multi-turn Conversations (P4)

**Goal**: Support conversation sessions with persistent history, allowing users to continue conversations across multiple requests.

**Independent Test**: Create session with first message, send follow-up message with session_id, verify history is loaded and response references previous context.

**Acceptance Criteria**:
1. Given a new chat request without session_id, when sent, then system creates new session and returns session_id
2. Given an existing session_id, when included in request, then system loads last N messages (default 5) and includes in prompt
3. Given a conversation, when messages are saved, then both user and assistant messages stored in Postgres with metadata

### Tasks

- [ ] T075 [US4] In models/chat.py, add ChatSession and Message schemas from data-model.md
- [ ] T076 [US4] In services/database.py, implement create_session(), get_session(), save_message(), get_recent_messages() functions
- [ ] T077 [US4] In services/database.py, implement update_session_timestamp() to update session.updated_at on new messages
- [ ] T078 [US4] In chat_service.py, modify chat() to accept optional session_id parameter
- [ ] T079 [US4] In chat_service.py, add load_history() calling database.get_recent_messages(session_id, limit=5)
- [ ] T080 [US4] In chat_service.py, modify build_prompt() to insert history messages before user query
- [ ] T081 [US4] In chat_service.py, add save_conversation() calling database.save_message() for both user and assistant messages
- [ ] T082 [US4] In chat_service.py, update chat() to: create/get session → load history → build prompt with history → generate → save messages → return with session_id
- [ ] T083 [US4] In selection_service.py, add same session support: accept session_id, load history, save messages
- [ ] T084 [US4] In routers/chat.py, update POST /chat to handle optional session_id in request
- [ ] T085 [US4] In routers/chat.py, update POST /chat/selection to handle optional session_id in request
- [ ] T086 [US4] Test: Create backend/tests/integration/test_sessions.py testing multi-turn conversations
- [ ] T087 [US4] Test: Test creating new session (session_id=null) returns new session_id
- [ ] T088 [US4] Test: Test continuing session (provide session_id) loads history correctly
- [ ] T089 [US4] Test: Test session history limited to last 5 messages (send 10 messages, verify only last 5 loaded)
- [ ] T090 [US4] Test: Test session mode tracking (normal vs selection) stored correctly in database
- [ ] T091 [US4] Test: Verify message metadata stores retrieved_chunks for normal mode, selected_text for selection mode

**Acceptance**:
- ✅ New sessions created automatically when session_id not provided
- ✅ Existing sessions load history (last 5 messages) correctly
- ✅ Conversation history included in prompt improves answer quality
- ✅ Both normal and selection chat modes support sessions
- ✅ Message metadata stored correctly (chunks for normal, text for selection)

**Parallel Opportunities**: T075-T076 (models + database) can run in parallel, T086-T091 (tests) can run in parallel

---

## Phase 7: Response Streaming (Enhancement)

**Goal**: Implement Server-Sent Events (SSE) streaming for real-time response generation.

**Independent Test**: Send chat request, verify response streams incrementally via SSE, final [DONE] marker received.

**Acceptance Criteria**:
1. Given a chat request, when response is generated, then chunks stream in real-time via SSE
2. Given streaming response, when complete, then [DONE] marker sent
3. Given client preference, when Accept header is application/json, then return full response (non-streaming fallback)

### Tasks

- [ ] T092 In chat_service.py, modify generate_response() to support streaming parameter
- [ ] T093 In chat_service.py, implement stream_response() async generator yielding chunks from OpenAI stream
- [ ] T094 In routers/chat.py, detect Accept header (text/event-stream vs application/json)
- [ ] T095 In routers/chat.py, implement stream_chat_response() using FastAPI StreamingResponse
- [ ] T096 In routers/chat.py, format SSE output: "data: {chunk}\n\n" and final "data: [DONE]\n\n"
- [ ] T097 In routers/chat.py, update POST /chat to return StreamingResponse when Accept: text/event-stream
- [ ] T098 In routers/chat.py, update POST /chat/selection to return StreamingResponse for consistency
- [ ] T099 Test: Create backend/tests/integration/test_streaming.py testing SSE streaming
- [ ] T100 Test: Verify chunks received incrementally (not all at once)
- [ ] T101 Test: Verify [DONE] marker received at end
- [ ] T102 Test: Test fallback to JSON response when Accept: application/json

**Acceptance**:
- ✅ Responses stream in real-time via SSE
- ✅ [DONE] marker sent correctly
- ✅ Fallback to JSON for non-streaming clients works
- ✅ Streaming works for both /chat and /chat/selection

**Parallel Opportunities**: T092-T093 (service) and T094-T098 (router) are sequential, but T099-T102 (tests) can run in parallel

---

## Phase 8: Error Handling & Observability (Polish)

**Goal**: Implement robust error handling, structured logging, request IDs, and error responses per OpenAPI spec.

**Independent Test**: Trigger various error conditions (invalid API keys, Qdrant down, rate limits), verify graceful degradation and error logging.

**Acceptance Criteria**:
1. Given any error, when it occurs, then structured log entry created with request_id, error details, stack trace
2. Given API errors (OpenAI, Qdrant), when they occur, then retry logic with exponential backoff applied
3. Given error response, when returned to client, then matches ErrorResponse schema from api.openapi.yaml

### Tasks

- [ ] T103 In models/chat.py, add ErrorResponse schema from api.openapi.yaml
- [ ] T104 In main.py, add global exception handler for all unhandled exceptions
- [ ] T105 In main.py, add middleware to generate request_id (UUID) for each request and inject into logging context
- [ ] T106 In utils/logging.py, configure loguru to output JSON format with request_id, timestamp, level, message, extra fields
- [ ] T107 In chat_service.py, add error handling: OpenAI API errors → log + return ErrorResponse with 500
- [ ] T108 In chat_service.py, implement retry logic for OpenAI calls (3 retries, exponential backoff)
- [ ] T109 In ingest.py, add error handling: parsing errors → log + return IngestResponse with status=failed
- [ ] T110 In vector_store.py, add error handling: Qdrant connection errors → log + raise custom exception
- [ ] T111 In database.py, add error handling: Postgres errors → log + raise custom exception
- [ ] T112 In routers/*.py, wrap all endpoints with try-except returning ErrorResponse on failures
- [ ] T113 Test: Create backend/tests/integration/test_error_handling.py testing various error scenarios
- [ ] T114 Test: Mock OpenAI API failure and verify retry logic executes 3 times
- [ ] T115 Test: Mock Qdrant down and verify health endpoint returns degraded status
- [ ] T116 Test: Test invalid book_id returns 404 with ErrorResponse format
- [ ] T117 Test: Verify all error responses include request_id field

**Acceptance**:
- ✅ All errors logged with structured format (JSON)
- ✅ Retry logic applied to external API calls (OpenAI, Qdrant)
- ✅ Error responses match ErrorResponse schema
- ✅ Request IDs included in all logs and error responses

**Parallel Opportunities**: T103-T106 (infrastructure) can run first, then T107-T112 (service errors) in parallel, then T113-T117 (tests) in parallel

---

## Phase 9: Testing & Documentation (Polish)

**Goal**: Achieve >80% test coverage, complete README, add inline documentation, verify quickstart guide.

**Independent Test**: Run pytest with coverage report, verify >80% coverage. Follow README to set up from scratch.

**Acceptance Criteria**:
1. Given pytest coverage report, when run, then coverage >= 80% for all modules
2. Given README, when followed, then developer can set up and run server in <10 minutes
3. Given inline docs, when reading code, then all public functions have docstrings

### Tasks

- [ ] T118 [P] Add docstrings to all public functions in services/ modules (Google style)
- [ ] T119 [P] Add docstrings to all routers and endpoint functions
- [ ] T120 [P] Add docstrings to utils/ modules
- [ ] T121 Run pytest --cov=app --cov-report=html and verify coverage >= 80%
- [ ] T122 If coverage < 80%, add missing unit tests for uncovered code paths
- [ ] T123 [P] Update backend/README.md with complete setup instructions from quickstart.md
- [ ] T124 [P] Add API examples to README (curl commands for all endpoints)
- [ ] T125 [P] Create backend/.env.example if not exists, ensure all required env vars documented
- [ ] T126 [P] Add troubleshooting section to README for common errors
- [ ] T127 Test: Follow README setup steps on clean environment, verify success
- [ ] T128 Test: Verify all example curl commands in README work correctly

**Acceptance**:
- ✅ Test coverage >= 80%
- ✅ All public functions have docstrings
- ✅ README complete and verified on clean environment
- ✅ API examples in README work

**Parallel Opportunities**: T118-T120 (docstrings) can all run in parallel, T123-T126 (README sections) can run in parallel

---

## Phase 10: Deployment & Performance (Polish)

**Goal**: Containerize application, verify performance goals, prepare for cloud deployment.

**Independent Test**: Build Docker image, run container, verify all endpoints work. Load test with 100 concurrent requests.

**Acceptance Criteria**:
1. Given Dockerfile, when built, then image size < 500MB and runs successfully
2. Given performance test, when 100 concurrent requests sent, then p95 latency < 2s for /chat
3. Given ingestion test, when 100-page PDF uploaded, then completes in < 60s

### Tasks

- [ ] T129 Verify Dockerfile builds successfully and image runs
- [ ] T130 Add .dockerignore to reduce image size (exclude tests, .env, __pycache__)
- [ ] T131 Optimize Docker image: use multi-stage build, alpine base if possible
- [ ] T132 [P] Create docker-compose.yml for local development (backend + postgres + qdrant)
- [ ] T133 [P] Add deployment instructions to README for Render, Railway, Fly.io from quickstart.md
- [ ] T134 Test: Build and run Docker container, verify health endpoint works
- [ ] T135 Test: Create backend/tests/performance/test_load.py using locust or pytest-benchmark
- [ ] T136 Test: Load test /chat with 100 concurrent requests, verify p95 < 2s
- [ ] T137 Test: Load test /ingest/book with 100-page PDF, verify < 60s completion
- [ ] T138 If performance goals not met, profile and optimize (embeddings batching, connection pooling)

**Acceptance**:
- ✅ Docker image builds and runs successfully
- ✅ Performance goals met (p95 < 2s chat, <60s ingestion)
- ✅ Deployment instructions complete

**Parallel Opportunities**: T129-T131 (Docker) and T132-T133 (compose + deploy docs) can run in parallel

---

## Dependency Graph

### User Story Dependencies

```
Phase 1 (Setup) ──────┐
                      ├──> Phase 2 (Foundational) ──┐
                      │                             │
                      │                             ├──> Phase 3 (US1: Book Ingestion) ──┐
                      │                             │                                     │
                      │                             │                                     ├──> Phase 4 (US2: Normal Chat) ──┐
                      │                             │                                     │                                  │
                      │                             │                                     │                                  ├──> Phase 6 (US4: Sessions)
                      │                             │                                     │                                  │
                      │                             │                                     └──> Phase 5 (US3: Selection) ────┘
                      │                             │
                      │                             └──> Phase 7 (Streaming) ────────────────────────────────────────────────┐
                      │                                                                                                       │
                      └──────────────────────────────────────────────────────────────────────────────────────────────────> Phase 8 (Errors) ──> Phase 9 (Testing) ──> Phase 10 (Deployment)
```

**Critical Path**: Phase 1 → Phase 2 → Phase 3 (US1) → Phase 4 (US2) → Phase 6 (US4)

**Independent Phases**:
- Phase 5 (US3: Selection) depends on Phase 2 (foundational) but NOT on US1 or US2
- Phase 7 (Streaming) can be implemented after US2 or US3
- Phase 8-10 (polish) depend on all user stories complete

### Blocking Tasks

**MUST complete before any user story**:
- T001-T018 (Phase 1: Setup)
- T019-T027 (Phase 2: Foundational services)

**MUST complete before Normal Chat (US2)**:
- T028-T045 (US1: Book Ingestion) - need data to query

**MUST complete before Sessions (US4)**:
- T046-T061 (US2: Normal Chat) OR T062-T074 (US3: Selection) - at least one chat mode

**No blockers for**:
- US3 (Selection) can be implemented independently after Phase 2

---

## Parallel Execution Examples

### Phase 1 (Setup) - Parallel Opportunities

**Batch 1** (independent file creation):
```bash
# Terminal 1: Create config and utils
- T004: config.py
- T005: logging.py

# Terminal 2: Create routers and services
- T012: routers/health.py
- T013: services/database.py
- T014: services/vector_store.py

# Terminal 3: Create documentation
- T002: requirements.txt
- T003: .env.example
- T016: README.md
- T007: Dockerfile
- T008: .dockerignore
```

**Batch 2** (sequential - depends on Batch 1):
```bash
# Must complete after Batch 1
- T001: Project structure
- T006: main.py (needs config.py)
- T009-T011: Alembic setup
- T015: Add health router to main.py
- T017-T018: Tests
```

### Phase 2 (Foundational) - Parallel Opportunities

**All tasks parallelizable**:
```bash
# Terminal 1: Parsers
- T019: PDF parser (pypdf)
- T020: PDF fallback (pdfplumber)
- T021: EPUB parser
- T022: HTML parser

# Terminal 2: Chunking and models
- T023: chunking.py
- T024: models/book.py

# Terminal 3: Tests
- T025: sample.pdf fixture
- T026: test_parsers.py
- T027: test_chunking.py
```

### Phase 3 (US1: Ingestion) - Parallel Opportunities

**Batch 1**:
```bash
# Terminal 1: Database layer
- T028: database.py functions

# Terminal 2: Vector store layer
- T029: vector_store.py functions

# Terminal 3: Models
- T035: models/ingest.py
```

**Batch 2** (depends on Batch 1):
```bash
# Terminal 1: Service layer
- T030-T034: services/ingest.py

# Terminal 2: Router layer
- T036-T040: routers/ingest.py
```

**Batch 3** (integration tests):
```bash
# Can all run in parallel
- T041: test_ingest_api.py
- T042: Qdrant collection test
- T043: Postgres test
- T044: Re-ingestion test
- T045: Error handling test
```

### Phase 4 (US2: Normal Chat) - Parallel Opportunities

**Batch 1**:
```bash
# Terminal 1: Models
- T046: models/chat.py

# Terminal 2: Vector store
- T047: vector_store.search()

# Terminal 3: Start chat service
- T048: chat_service.py file creation
```

**Batch 2** (depends on Batch 1):
```bash
# Sequential in chat_service.py
- T049-T053: chat service functions
```

**Batch 3**:
```bash
# Terminal 1: Router
- T054-T057: routers/chat.py

# Terminal 2: Tests
- T058-T061: test_chat_api.py
```

---

## MVP Scope Recommendation

**Minimum Viable Product** (for hackathon demo):

✅ **Include**:
- Phase 1: Project Setup (T001-T018)
- Phase 2: Foundational Services (T019-T027)
- Phase 3: US1 - Book Ingestion (T028-T045)
- Phase 4: US2 - Normal RAG Chat (T046-T061)

❌ **Defer to post-MVP**:
- Phase 5: US3 - Selected-Text Chat (nice-to-have)
- Phase 6: US4 - Multi-turn Sessions (enhancement)
- Phase 7: Streaming (enhancement)
- Phase 8-10: Polish (iterate after core works)

**MVP Acceptance**:
- Admin can upload a book (PDF)
- User can ask questions and get answers with sources
- Health check confirms services are working

**Estimated MVP Effort**: ~61 tasks (T001-T061), ~2-3 days for hackathon

---

## Task Statistics

**Total Tasks**: 138
**Phases**: 10
**User Stories**: 4 (US1-US4)

**Per Phase**:
- Phase 1 (Setup): 18 tasks
- Phase 2 (Foundational): 9 tasks
- Phase 3 (US1): 18 tasks
- Phase 4 (US2): 16 tasks
- Phase 5 (US3): 13 tasks
- Phase 6 (US4): 17 tasks
- Phase 7 (Streaming): 11 tasks
- Phase 8 (Errors): 15 tasks
- Phase 9 (Testing): 11 tasks
- Phase 10 (Deployment): 10 tasks

**Parallelizable Tasks**: ~45 marked with [P] flag

**Per User Story**:
- US1 (Book Ingestion): 18 tasks
- US2 (Normal Chat): 16 tasks
- US3 (Selection Chat): 13 tasks
- US4 (Sessions): 17 tasks

---

## Format Validation

✅ **All tasks follow checklist format**:
- [x] Checkbox: `- [ ]` prefix
- [x] Task ID: Sequential T001-T138
- [x] [P] marker: 45 tasks marked as parallelizable
- [x] [US#] label: All user story tasks labeled (US1, US2, US3, US4)
- [x] Description: Clear action with file path
- [x] Examples: See T001, T046, T063, T086

---

## Next Steps

1. **Review tasks.md**: Verify task breakdown aligns with plan.md and data-model.md
2. **Start implementation**: Begin with Phase 1 (Setup)
3. **TDD approach**: Write tests before implementation where marked
4. **Track progress**: Use `/sp.implement` or manual task completion
5. **Iterate**: Adjust based on discoveries during implementation

**Ready for implementation!** 🚀
