# RAG Chatbot for Physical AI Humanoid Robotics Book

## 📚 Ye Kya Hai?

Ye ek complete **RAG (Retrieval-Augmented Generation) chatbot** hai jo aapki book se questions answer karta hai using:
- **FastAPI** - Python backend framework
- **Qdrant** - Vector database for semantic search
- **OpenAI** - Embeddings aur GPT-4 for answers
- **Simple HTML/CSS/JS** - Frontend UI

## 🚀 Setup Kaise Karein (Step-by-Step)

### Step 1: Prerequisites Install Karo

**Zaroorat:**
- Python 3.11+ installed hona chahiye
- Docker installed hona chahiye (Qdrant ke liye)
- OpenAI API key (https://platform.openai.com/api-keys se)

**Check karo:**
```bash
python --version  # 3.11+ hona chahiye
docker --version  # Docker installed hai ya nahi
```

### Step 2: Repository Clone/Download Karo

Agar git hai:
```bash
git clone <your-repo-url>
cd Physical-AI-Humanoid-Robotics-
```

### Step 3: Backend Setup Karo

#### 3.1 Virtual Environment Banao (Optional but Recommended)

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### 3.2 Dependencies Install Karo

```bash
pip install -r requirements.txt
```

Ye sab install hoga:
- FastAPI, Uvicorn (web server)
- OpenAI SDK (embeddings + chat)
- Qdrant client (vector database)
- pypdf, ebooklib, beautifulsoup4 (document parsing)
- tiktoken (token counting)

#### 3.3 Environment Variables Setup Karo

1. `.env.example` file ko copy karke `.env` banao:

```bash
copy .env.example .env  # Windows
# ya
cp .env.example .env    # Linux/Mac
```

2. `.env` file ko edit karo aur apni API keys daalo:

```env
# OpenAI API Key (https://platform.openai.com/api-keys se lo)
OPENAI_API_KEY=sk-your-actual-api-key-here

# Qdrant Settings (local Docker ke liye ye default rahein)
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# Models
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4

# Chunking
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

**Important:** OpenAI API key zaroor daalo, warna kaam nahi karega!

### Step 4: Qdrant Vector Database Start Karo

Backend directory mein ho toh:

```bash
# Docker Compose se Qdrant start karo
docker-compose up -d
```

Ye command:
- Qdrant container start karega
- Port 6333 par API available hoga
- Port 6334 par Web UI available hoga

**Check karo:**
- Browser mein jao: http://localhost:6334
- Qdrant dashboard dikhna chahiye

### Step 5: Backend Server Start Karo

```bash
# Backend directory mein ho toh
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Ya direct:**
```bash
python app/main.py
```

**Success message dikhe toh:**
```
RAG Chatbot API Starting...
OpenAI Model: gpt-4
Embedding Model: text-embedding-3-small
Qdrant URL: http://localhost:6333
Docs: http://0.0.0.0:8000/docs
```

**API Test karo:**
- Browser mein jao: http://localhost:8000/docs
- Swagger UI dikhe toh sab theek hai!
- Health check: http://localhost:8000/health

### Step 6: Frontend Open Karo

1. Naya terminal kholo
2. Frontend directory mein jao:

```bash
cd ../frontend
```

3. Simple HTTP server start karo:

**Option 1: Python (already installed hai):**
```bash
python -m http.server 3000
```

**Option 2: Node.js (agar installed hai):**
```bash
npx http-server -p 3000
```

**Option 3: VS Code:**
- Right-click `index.html` -> "Open with Live Server"

4. Browser mein jao: http://localhost:3000

## 📖 Kaise Use Karein?

### Option 1: Normal RAG Chat (Full Book Search)

1. **Book Upload:**
   - "Upload Your Book" section mein file select karo (PDF/HTML/EPUB)
   - "Upload Book" button click karo
   - Wait karo jab tak chunks ban jaayein aur embeddings generate ho

2. **Chat:**
   - "Ask Questions" section mein type karo
   - Enter dabao ya "Send" click karo
   - AI answer dega with sources (proof)

**Example Questions:**
- "What is Physical AI?"
- "Explain ROS 2 architecture"
- "How does digital twin work?"

### Option 2: Selected Text Q&A

1. "📝 Selected Text Q&A" mode select karo
2. Book ka koi portion copy-paste karo text box mein
3. Question type karo about that text
4. Answer milega sirf us text ke basis par (Qdrant use nahi hoga)

**Use Case:** Jab aapko book ke ek specific section ke baare mein detail chahiye.

## 🔧 API Endpoints

### 1. Health Check
```bash
GET http://localhost:8000/health
```
Response: Qdrant aur OpenAI working hain ya nahi

### 2. Upload Book
```bash
POST http://localhost:8000/ingest/book
Content-Type: multipart/form-data

Body:
- file: your-book.pdf
- book_id: optional
```

Response:
```json
{
  "book_id": "uuid",
  "title": "Book Title",
  "total_chunks": 150,
  "status": "completed"
}
```

### 3. Normal Chat
```bash
POST http://localhost:8000/chat/
Content-Type: application/json

{
  "book_id": "uuid",
  "message": "What is Physical AI?",
  "session_id": "optional-uuid"
}
```

Response:
```json
{
  "session_id": "uuid",
  "response": "Physical AI refers to...",
  "sources": [
    {
      "chunk_id": "uuid",
      "text": "...",
      "score": 0.95,
      "metadata": {}
    }
  ]
}
```

### 4. Selection Chat
```bash
POST http://localhost:8000/chat/selection
Content-Type: application/json

{
  "selected_text": "Your selected text here...",
  "question": "What does this mean?",
  "session_id": "optional-uuid"
}
```

Response:
```json
{
  "session_id": "uuid",
  "response": "This text explains..."
}
```

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings aur env variables
│   ├── models/              # Pydantic data models
│   │   ├── book.py          # Book aur chunk models
│   │   └── chat.py          # Chat request/response models
│   ├── services/            # Business logic
│   │   ├── ingest.py        # Book upload aur processing
│   │   ├── vector_store.py  # Qdrant operations
│   │   ├── embedding.py     # OpenAI embeddings
│   │   └── chat_service.py  # RAG chat logic
│   ├── routers/             # API endpoints
│   │   ├── health.py        # Health check
│   │   ├── ingest.py        # Upload endpoint
│   │   └── chat.py          # Chat endpoints
│   └── utils/               # Helper functions
│       ├── parsers.py       # PDF/HTML/EPUB parsing
│       └── chunking.py      # Text chunking
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── docker-compose.yml      # Qdrant setup
└── README.md              # Ye file!

frontend/
├── index.html             # Main HTML file
├── static/
│   ├── css/
│   │   └── style.css      # Styling
│   └── js/
│       └── app.js         # Frontend logic
```

## 🧪 Testing

### Manual Testing

1. **Health Check:**
```bash
curl http://localhost:8000/health
```

2. **Upload Book:**
```bash
curl -X POST -F "file=@sample.pdf" http://localhost:8000/ingest/book
```

3. **Chat:**
```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"book_id":"your-book-id", "message":"What is ROS 2?"}'
```

### Swagger UI se Testing

1. http://localhost:8000/docs par jao
2. Koi bhi endpoint expand karo
3. "Try it out" button click karo
4. Parameters enter karo
5. "Execute" click karo

## 💡 How It Works (Roman Urdu Explanation)

### 1. Book Upload (Ingestion)

**Process:**
```
PDF File
  ↓
Parse karo (text extract karo)
  ↓
Chunks banao (1000 tokens each, 200 overlap)
  ↓
Har chunk ka embedding generate karo (OpenAI)
  ↓
Qdrant mein store karo (vector database)
```

**Example:**
- Book: 200 pages
- Chunks: ~150 chunks ban jayenge
- Embeddings: 150 vectors (har ek 1536 dimensions)
- Storage: Qdrant mein with metadata (page number, etc.)

### 2. RAG Chat (Normal)

**Process:**
```
User Question: "What is Physical AI?"
  ↓
Question ko embed karo (vector banao)
  ↓
Qdrant mein search karo (similar chunks dhundo)
  ↓
Top 5 relevant chunks retrieve karo
  ↓
Chunks + Question ko GPT-4 ko do
  ↓
GPT-4 answer generate kare (sirf chunks ke basis par)
  ↓
Answer + Sources user ko dikha do
```

**Key Point:** Answer hamesha book se aata hai, GPT-4 apna knowledge use nahi karta.

### 3. Selection Chat

**Process:**
```
User selected text copy kare
  ↓
Question poochen
  ↓
Selected text + Question directly GPT-4 ko
  ↓
Answer generate ho (Qdrant use nahi hua)
```

**Use Case:** Jab specific paragraph ke baare mein detail chahiye.

## 🔥 Common Issues & Solutions

### 1. "Module not found" Error
```bash
# Solution: Virtual environment activate karo aur requirements install karo
pip install -r requirements.txt
```

### 2. "Connection refused" to Qdrant
```bash
# Solution: Qdrant container start karo
docker-compose up -d

# Check karo running hai ya nahi
docker ps
```

### 3. "Invalid API key" Error
```bash
# Solution: .env file check karo, OpenAI key sahi hai ya nahi
# Key yahan se lo: https://platform.openai.com/api-keys
```

### 4. CORS Error (Frontend se backend call nahi ho rahi)
```python
# backend/app/main.py mein CORS origins check karo
# Frontend URL add karo:
allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"]
```

### 5. Slow Embedding Generation
```python
# .env mein embedding model change karo
EMBEDDING_MODEL=text-embedding-3-small  # Sasta aur fast
# ya
EMBEDDING_MODEL=text-embedding-ada-002  # Purana but reliable
```

### 6. "This information is not available in the book"
**Reasons:**
- Book properly upload nahi hua
- Question book ke scope se bahar hai
- Chunks mein relevant information nahi mila

**Solutions:**
- Book re-upload karo
- Question rephrased karke dobara poocho
- Selected text Q&A mode use karo specific text ke liye

## 💰 Cost Estimation (OpenAI)

### Embedding Costs
- Model: text-embedding-3-small
- Price: $0.00002 per 1K tokens
- Example: 200-page book = ~150 chunks = ~$0.003

### Chat Costs
- Model: GPT-4
- Price: ~$0.03 per 1K tokens (input + output)
- Example: 10 questions = ~$0.10

**Total for testing:** ~$0.20-0.50

**Tip:** Development mein `gpt-3.5-turbo` use karo (10x cheaper)

## 🚀 Deployment (Optional)

### Option 1: Local Deployment
- Already done! (jaise abhi chal raha hai)

### Option 2: Qdrant Cloud (free tier)
1. https://cloud.qdrant.io par jao
2. Free cluster banao
3. API key aur URL copy karo
4. `.env` mein update karo:
```env
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your-api-key
```

### Option 3: Full Cloud Deployment
**Backend:** Render, Railway, Fly.io
**Frontend:** Vercel, Netlify, GitHub Pages

## 📚 Next Steps

1. ✅ Basic setup complete
2. 📖 Book upload karke test karo
3. 💬 Questions poocho aur answers dekho
4. 🎨 Frontend customize karo (optional)
5. 🚀 Deploy karo (optional)

## 🤝 Support

**Issues:**
- Qdrant dashboard: http://localhost:6334
- API docs: http://localhost:8000/docs
- Logs check karo terminal mein

**Debugging:**
- Backend logs: Terminal mein dikhengi jahan server chala hua hai
- Frontend logs: Browser console (F12)
- Qdrant logs: `docker logs qdrant_vectordb`

## 📝 Notes

- **Token Limits:** GPT-4 ka context window 8K hai, long conversations mein trimming hogi
- **Chunk Overlap:** 200 tokens overlap se better retrieval hoti hai
- **Similarity Score:** >0.8 = very relevant, <0.5 = not very relevant
- **Book Formats:** PDF best works, HTML bhi theek, EPUB kabhi kabhi issues

---

**Happy Chatting! 🎉**

Agar koi problem aaye toh pehle:
1. Health check karo
2. Logs dekho
3. Docker/Qdrant running check karo
4. API keys verify karo
