---
id: 001
title: RAG Backend Implementation Plan
stage: plan
date: 2025-12-15
surface: agent
model: claude-sonnet-4-5
feature: 001-physical-ai-book
branch: 001-physical-ai-book
user: Cs
command: /sp.plan
labels: ["rag", "backend", "architecture", "fastapi", "openai", "qdrant", "postgres"]
links:
  spec: specs/001-physical-ai-book/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-physical-ai-book/plan.md
  - specs/001-physical-ai-book/research.md
  - specs/001-physical-ai-book/data-model.md
  - specs/001-physical-ai-book/contracts/api.openapi.yaml
  - specs/001-physical-ai-book/quickstart.md
tests:
  - (Phase 2: Tests will be generated during /sp.tasks)
---

## Prompt

You are an expert AI-native software engineer.

I want a high-level **implementation plan** for a hackathon project:

Project: **RAG Chatbot Backend for AI-native Book Platform**

Requirements:
1. **RAG Chatbot** using OpenAI Agents / ChatKit SDK.
2. Supports **normal Q&A** (semantic search on full book) and **selected-text Q&A** (only user-selected text).
3. Backend: FastAPI, Neon Serverless Postgres (metadata, user chats), Qdrant Cloud (vector search).
4. Features:
   - `/ingest/book` API: PDF/HTML/EPUB → chunk → embed → store in Qdrant.
   - `/chat` API: normal RAG question-answer.
   - `/chat/selection` API: selected-text Q&A.
   - Multi-turn reasoning agent with book-aware context.
5. Constraints:
   - Selected-text Q&A must **not call Qdrant**, only use the provided text.
   - Hackathon-ready, modular, production-oriented.

Please provide:
- Folder structure
- Key backend modules
- API endpoints
- Data flow diagrams or descriptions
- Step-by-step implementation plan

## Response snapshot

Generated comprehensive implementation plan with following artifacts:

### 1. plan.md (Main Implementation Plan)
- **Technical Context**: Python 3.11+, FastAPI, OpenAI SDK, Qdrant Cloud, Neon Postgres
- **Performance Goals**: <60s PDF ingestion, <2s chat latency, <1s selection latency
- **Architecture**: Monolithic backend with modular services (ingest, chat, selection, vector_store, database)
- **Key Decisions**:
  - text-embedding-3-small (cost-effective, 1536 dims)
  - 1000 token chunks with 200 overlap
  - Custom agent loop (no framework overhead)
  - Separate SelectionService to enforce no-Qdrant constraint
  - Postgres for metadata, Qdrant for vectors (separation of concerns)
  - Streaming responses via SSE for real-time UX
- **Data Flows**: Detailed diagrams for ingestion, normal chat, selection chat
- **Risk Analysis**: Qdrant latency, OpenAI costs, PDF parsing failures with mitigations
- **ADR Suggestions**: 3 architectural decisions detected for documentation

### 2. research.md (Phase 0: Technology Decisions)
Resolved 7 research tasks with rationale and alternatives:
- Document parsing: pypdf (primary) + pdfplumber (fallback)
- Chunking: Fixed 1000 tokens, 200 overlap with tiktoken
- Embeddings: text-embedding-3-small (62.3% MTEB, $0.02/1M tokens)
- RAG pattern: Stateful with DB-persisted history, load last 5 turns
- Qdrant: Single collection, cosine distance, book_id filtering
- Agent: Custom loop (vs OpenAI Assistants API - cost/control trade-off)
- Schema: Normalized Postgres with JSONB flexibility

Clarified 3 unknowns:
- Selected-text Q&A supports multi-turn (same as normal mode)
- Book ingestion is idempotent (re-ingest allowed)
- Streaming responses via SSE

### 3. data-model.md (Phase 1: Entities & Schemas)
Defined 4 core entities with validation rules:
- **Book**: UUID, title, author, metadata (JSONB), total_chunks
- **BookChunk**: UUID, book_id FK, chunk_index, text (Postgres + Qdrant)
- **ChatSession**: UUID, book_id FK, mode (normal/selection), timestamps
- **Message**: UUID, session_id FK, role (user/assistant), content, metadata

Relationships:
- Book 1→N BookChunk (cascade delete)
- Book 1→N ChatSession
- ChatSession 1→N Message

Storage strategy:
- Postgres: Structured metadata, chat history (ACID transactions)
- Qdrant: Vector embeddings, semantic search (payload: text + metadata)

Pydantic models for API validation with full schema definitions.

### 4. contracts/api.openapi.yaml (Phase 1: API Specification)
OpenAPI 3.1 spec with 4 endpoints:
- **GET /health**: Service status (postgres, qdrant, openai)
- **POST /ingest/book**: Upload PDF/HTML/EPUB, returns book_id + total_chunks
- **POST /chat**: Normal RAG with vector search, returns response + sources
- **POST /chat/selection**: Text-only Q&A (no Qdrant), returns response

Request/response schemas, error handling, SSE streaming support documented.

### 5. quickstart.md (Phase 1: Setup Guide)
10-minute setup guide:
- Prerequisites: Python 3.11+, OpenAI/Qdrant/Neon API keys
- 5-step setup: clone, install deps, configure .env, run migrations, start server
- Testing examples: health check, book ingestion, normal chat, multi-turn, selection chat
- Troubleshooting: Common issues (connection errors, API keys, memory)
- Deployment: Docker + cloud platforms (Render, Railway, Fly.io)

## Outcome

- ✅ Impact: Complete implementation plan for hackathon RAG backend with architecture, technology choices, data model, API contracts, and quickstart guide
- 🧪 Tests: Test strategy defined in plan; actual tests to be generated in Phase 2 (/sp.tasks)
- 📁 Files: Created 5 design artifacts (plan.md, research.md, data-model.md, api.openapi.yaml, quickstart.md)
- 🔁 Next prompts: Run /sp.tasks to generate executable implementation tasks with TDD approach
- 🧠 Reflection: Architecture enforces selected-text constraint at code level (separate service), balances cost vs quality (text-embedding-3-small, gpt-4o-mini for dev), ready for hackathon timeline

## Evaluation notes (flywheel)

- Failure modes observed: None during planning; potential runtime failures addressed in risk analysis (Qdrant latency, OpenAI costs, PDF parsing)
- Graders run and results (PASS/FAIL): Constitution check PASS (modularity, testability, security, simplicity principles followed)
- Prompt variant (if applicable): Standard /sp.plan workflow with user-provided RAG requirements
- Next experiment (smallest change to try): Generate tasks.md with /sp.tasks, validate task breakdown granularity for hackathon velocity
