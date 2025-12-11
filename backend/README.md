# RAG Chatbot Backend

FastAPI backend for the Physical AI & Humanoid Robotics book chatbot with Retrieval-Augmented Generation (RAG).

## Features

- **RAG Pipeline**: OpenAI embeddings + GPT-4 for context-aware responses
- **Vector Search**: Qdrant Cloud for semantic search
- **Chat History**: Neon Serverless Postgres for conversation persistence
- **Text Selection**: Answer questions about user-selected text
- **Session Management**: Multi-session support with history

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and add your credentials:

```bash
cp .env.example .env
```

**Required credentials:**
- **OpenAI API Key**: https://platform.openai.com/api-keys
- **Qdrant Cloud**: https://cloud.qdrant.io (Free Tier)
- **Neon Postgres**: https://neon.tech (Free Tier)

### 3. Index Documents

```bash
python scripts/index_documents.py
```

This will scan all book chapters, chunk them, generate embeddings, and upload to Qdrant.

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

API will be available at: http://localhost:8000

## API Endpoints

- `GET /` - Health check
- `POST /chat` - Send chat message
- `GET /chat/history/{session_id}` - Get chat history
- `POST /chat/clear/{session_id}` - Clear session
- `GET /health` - Detailed health status

## Deployment

### Railway.app
1. Create account at https://railway.app
2. Connect GitHub repo
3. Add environment variables
4. Deploy

### Docker
```bash
docker build -t rag-chatbot .
docker run -p 8000:8000 --env-file .env rag-chatbot
```

## License

MIT
