# Quickstart Guide: RAG Chatbot Backend

**Feature**: RAG Chatbot Backend for AI-native Book Platform
**Version**: 1.0
**Updated**: 2025-12-15

## Overview

This guide walks you through setting up and running the RAG chatbot backend locally in under 10 minutes.

---

## Prerequisites

### Required

- **Python 3.11+** (check: `python --version`)
- **pip** (package manager, included with Python)
- **Git** (for cloning repository)

### API Keys (Required)

You'll need accounts and API keys for:

1. **OpenAI** (embeddings + chat completions)
   - Sign up: https://platform.openai.com/signup
   - Get API key: https://platform.openai.com/api-keys
   - Cost estimate: ~$0.10 for development testing

2. **Qdrant Cloud** (vector database)
   - Sign up: https://cloud.qdrant.io/
   - Create cluster: Free tier (1GB) sufficient for MVP
   - Get API key + cluster URL from dashboard

3. **Neon Serverless Postgres** (metadata + chat history)
   - Sign up: https://neon.tech/
   - Create project: Free tier sufficient
   - Get connection string from dashboard

### Optional

- **Docker** (for containerized deployment)
- **Postman** or **curl** (for testing APIs)

---

## Setup Steps

### 1. Clone Repository

```bash
git clone https://github.com/your-org/physical-ai-book.git
cd physical-ai-book
```

### 2. Install Dependencies

Navigate to backend directory and install Python packages:

```bash
cd backend
pip install -r requirements.txt
```

**requirements.txt** (includes):
```
fastapi==0.104.1
openai==1.3.0
qdrant-client==1.7.0
psycopg[binary]==3.1.18
pypdf==3.17.0
ebooklib==0.18
beautifulsoup4==4.12.2
pydantic==2.5.0
pydantic-settings==2.1.0
uvicorn[standard]==0.24.0
python-multipart==0.0.6
tiktoken==0.5.2
loguru==0.7.2
alembic==1.13.1
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

### 3. Configure Environment Variables

Copy example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```bash
# OpenAI
OPENAI_API_KEY=sk-proj-...  # Your OpenAI API key

# Qdrant Cloud
QDRANT_URL=https://your-cluster.qdrant.io  # Your Qdrant cluster URL
QDRANT_API_KEY=...  # Your Qdrant API key

# Neon Postgres
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/dbname?sslmode=require

# Application Settings
ENVIRONMENT=development  # development | production
LOG_LEVEL=INFO  # DEBUG | INFO | WARNING | ERROR
EMBEDDING_MODEL=text-embedding-3-small  # OpenAI embedding model
CHAT_MODEL=gpt-4o-mini  # OpenAI chat model (cheaper for dev)
CHUNK_SIZE=1000  # Token count per chunk
CHUNK_OVERLAP=200  # Token overlap between chunks
TOP_K_CHUNKS=5  # Number of chunks to retrieve for RAG
```

**.env.example** (template):
```bash
# OpenAI API Configuration
OPENAI_API_KEY=sk-proj-YOUR_KEY_HERE

# Qdrant Vector Database
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=YOUR_QDRANT_KEY_HERE
QDRANT_COLLECTION_NAME=physical_ai_book_chunks

# Neon Postgres Database
DATABASE_URL=postgresql://user:password@host:port/dbname?sslmode=require

# Application Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
CORS_ORIGINS=["http://localhost:3000"]  # Frontend origin (JSON array)

# OpenAI Models
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4o-mini  # Use gpt-4o-mini for dev (cheaper), gpt-4 for production

# RAG Configuration
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K_CHUNKS=5
MAX_HISTORY_MESSAGES=10  # Max conversation history to load
```

### 4. Initialize Database

Run Alembic migrations to create Postgres tables:

```bash
# From backend/ directory
alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001_initial_schema
```

**Note**: Qdrant collection is created automatically on first use (see `app/services/vector_store.py`).

### 5. Start Development Server

Run FastAPI with auto-reload:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Expected output:
```
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Server is now running at **http://localhost:8000**

---

## Testing the API

### 1. Health Check

Verify all services are connected:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "services": {
    "postgres": "up",
    "qdrant": "up",
    "openai": "up"
  },
  "timestamp": "2025-12-15T10:30:00Z"
}
```

### 2. Ingest a Book

Upload a PDF file to create vector embeddings:

**Using curl:**
```bash
curl -X POST "http://localhost:8000/ingest/book" \
  -F "file=@/path/to/physical-ai-book.pdf"
```

**Using Python requests:**
```python
import requests

with open("physical-ai-book.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post("http://localhost:8000/ingest/book", files=files)

print(response.json())
```

Expected response (takes 30-60 seconds for ~100 pages):
```json
{
  "book_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Physical AI Humanoid Robotics",
  "total_chunks": 842,
  "status": "completed"
}
```

**Save the `book_id`** for chat requests.

### 3. Normal RAG Chat

Ask a question using semantic search:

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "What is Physical AI?"
  }'
```

Expected response:
```json
{
  "session_id": "660e8400-e29b-41d4-a716-446655440001",
  "response": "Physical AI refers to artificial intelligence systems that interact with the physical world through robotic embodiment. Unlike traditional digital AI, Physical AI must handle real-world uncertainty from sensors, dynamics, and environmental complexity...",
  "sources": [
    {
      "chunk_id": "770e8400-e29b-41d4-a716-446655440002",
      "text": "Physical AI combines machine learning with robotics...",
      "score": 0.92,
      "metadata": {
        "page_number": 12,
        "chapter": "Introduction"
      }
    }
  ],
  "timestamp": "2025-12-15T10:35:00Z"
}
```

**Save the `session_id`** for multi-turn conversations.

### 4. Multi-Turn Conversation

Continue the conversation using `session_id`:

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "660e8400-e29b-41d4-a716-446655440001",
    "book_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "What are the main challenges?"
  }'
```

The assistant will use conversation history to understand "challenges" refers to Physical AI.

### 5. Selected-Text Chat

Ask about specific highlighted text (no vector search):

```bash
curl -X POST "http://localhost:8000/chat/selection" \
  -H "Content-Type: application/json" \
  -d '{
    "selected_text": "ROS 2 uses a Data Distribution Service (DDS) middleware for communication between nodes.",
    "question": "What is DDS?"
  }'
```

Expected response:
```json
{
  "session_id": "660e8400-e29b-41d4-a716-446655440003",
  "response": "DDS (Data Distribution Service) is a middleware layer that ROS 2 uses for inter-process communication...",
  "timestamp": "2025-12-15T10:40:00Z"
}
```

**Note**: No `sources` field (selected-text mode doesn't search Qdrant).

---

## Interactive API Documentation

FastAPI auto-generates interactive API docs:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Use Swagger UI to test endpoints directly in the browser.

---

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Environment settings (loads .env)
│   ├── models/              # Pydantic schemas
│   │   ├── book.py
│   │   ├── chat.py
│   │   └── user.py
│   ├── services/            # Business logic
│   │   ├── ingest.py        # Document parsing, chunking, embedding
│   │   ├── vector_store.py  # Qdrant operations
│   │   ├── chat_service.py  # RAG orchestration
│   │   ├── selection_service.py  # Selected-text Q&A
│   │   └── database.py      # Postgres operations
│   ├── routers/             # API endpoints
│   │   ├── ingest.py
│   │   ├── chat.py
│   │   └── health.py
│   └── utils/               # Helpers
│       ├── chunking.py
│       ├── parsers.py
│       └── logging.py
├── tests/                   # Test suite
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── alembic/                 # Database migrations
├── .env                     # Environment variables (DO NOT COMMIT)
├── .env.example             # Template for .env
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container image (for deployment)
└── README.md
```

---

## Running Tests

### Unit Tests

Test individual services (parsers, chunking, database ops):

```bash
pytest tests/unit/ -v
```

### Integration Tests

Test full API endpoints (requires running server + test DB):

```bash
# Start test server in background
uvicorn app.main:app --port 8001 &

# Run integration tests
pytest tests/integration/ -v

# Stop test server
pkill -f "uvicorn app.main:app --port 8001"
```

### Test Coverage

```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html  # View coverage report
```

---

## Common Issues & Troubleshooting

### Issue: "Connection refused" when calling API

**Cause**: Server not running or wrong port

**Solution**:
```bash
# Check if server is running
lsof -i :8000

# Restart server
uvicorn app.main:app --reload
```

### Issue: "OpenAI API key is invalid"

**Cause**: Missing or incorrect `OPENAI_API_KEY` in `.env`

**Solution**:
1. Verify key in `.env` matches your OpenAI dashboard
2. Check for extra spaces or newlines
3. Restart server after updating `.env`

### Issue: "Qdrant connection failed"

**Cause**: Incorrect `QDRANT_URL` or `QDRANT_API_KEY`

**Solution**:
1. Verify Qdrant cluster is active in dashboard
2. Check URL format: `https://your-cluster.qdrant.io` (no trailing slash)
3. Ensure API key has read/write permissions

### Issue: "Database connection failed"

**Cause**: Invalid Neon Postgres connection string

**Solution**:
1. Copy exact connection string from Neon dashboard
2. Ensure `?sslmode=require` is appended
3. Check if database is active (Neon auto-suspends after inactivity)

### Issue: "File upload too large"

**Cause**: FastAPI default body size limit (16MB)

**Solution**: Add to `app/main.py`:
```python
app = FastAPI()
app.router.route_class = LargeBodyRoute  # Custom route for large uploads
```

### Issue: "Out of memory during ingestion"

**Cause**: Large PDF loaded into memory at once

**Solution**:
- Chunk file reading in `app/utils/parsers.py`
- Use streaming upload for files >50MB
- Increase server memory allocation

---

## Deployment

### Docker

Build and run in container:

```bash
# Build image
docker build -t rag-backend .

# Run container
docker run -p 8000:8000 --env-file .env rag-backend
```

### Cloud Platforms

**Render** (recommended for hackathons):
1. Connect GitHub repo
2. Select "Web Service"
3. Build command: `pip install -r backend/requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables from `.env`

**Railway**:
```bash
railway login
railway init
railway up
```

**Fly.io**:
```bash
fly launch
fly deploy
```

---

## Next Steps

1. **Integrate with Frontend**: Update Next.js app to call backend APIs
2. **Add Authentication**: Implement API key or JWT auth (see `components/securitySchemes` in OpenAPI spec)
3. **Monitor Performance**: Add Prometheus metrics, OpenTelemetry tracing
4. **Optimize Costs**: Switch to `gpt-4o-mini` for production (10x cheaper than `gpt-4`)
5. **Improve Retrieval**: Experiment with hybrid search (keyword + vector), re-ranking
6. **Add Features**: User feedback, conversation export, multi-book support

---

## Resources

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **OpenAI API**: https://platform.openai.com/docs/
- **Qdrant Docs**: https://qdrant.tech/documentation/
- **Neon Docs**: https://neon.tech/docs/
- **RAG Best Practices**: https://www.pinecone.io/learn/retrieval-augmented-generation/

---

## Support

For issues or questions:
- **GitHub Issues**: https://github.com/your-org/physical-ai-book/issues
- **Email**: support@example.com
- **Documentation**: See `specs/001-physical-ai-book/plan.md` for architecture details

---

**Status**: Quickstart guide complete
**Estimated Setup Time**: 10 minutes
**Next**: Run `/sp.tasks` to generate implementation tasks
