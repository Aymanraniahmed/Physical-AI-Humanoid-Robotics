# 🚀 Complete Setup Guide - RAG Chatbot with Gemini

## ✅ Kya Kya Bana Hai?

1. ✅ **Backend**: FastAPI with **Google Gemini** (FREE!)
2. ✅ **Vector DB**: Qdrant
3. ✅ **Frontend**: Chatbot widget integrated in your Docusaurus website
4. ✅ **Features**: Book upload, RAG Q&A, Selected text Q&A

---

## 📋 Prerequisites

- Python 3.11+
- Docker (for Qdrant)
- Node.js 18+ (for Docusaurus)
- Google Gemini API Key (FREE)

---

## 🔑 STEP 1: Get Gemini API Key (2 minutes)

1. Yahan jao: https://makersuite.google.com/app/apikey
2. "Create API Key" click karo
3. Key copy karo

---

## 🖥️ STEP 2: Backend Setup (5 minutes)

```bash
# 1. Backend folder mein jao
cd backend

# 2. Virtual environment banao (optional)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Dependencies install karo
pip install -r requirements.txt

# 4. Environment file banao
copy .env.example .env  # Windows
# cp .env.example .env    # Linux/Mac

# 5. .env file edit karo aur API key daalo
# GEMINI_API_KEY=your-actual-key-here

# 6. Qdrant start karo
docker-compose up -d

# 7. Backend start karo
python -m uvicorn app.main:app --reload
```

**✓ Backend running:** http://localhost:8000

---

## 🌐 STEP 3: Frontend Setup (3 minutes)

```bash
# 1. Main project folder mein jao (Docusaurus)
cd Physical-AI-Humanoid-Robotics-

# 2. Dependencies install karo (agar nahi kiye)
npm install

# 3. Development server start karo
npm start
```

**✓ Website running:** http://localhost:3000

---

## 🎉 STEP 4: Use Karo!

### Option 1: Docusaurus Website Pe

1. Browser mein jao: **http://localhost:3000**
2. Bottom-right corner mein **purple chat button** (💬) dikhai dega
3. Click karo
4. Book upload karo (PDF/HTML/EPUB)
5. Questions poocho!

### Option 2: Direct API Test

```bash
# Health check
curl http://localhost:8000/health

# Book upload
curl -X POST -F "file=@yourbook.pdf" http://localhost:8000/ingest/book

# Chat
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{"book_id":"your-book-id", "message":"What is Physical AI?"}'
```

---

## 📁 Project Structure

```
Physical-AI-Humanoid-Robotics-/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # Entry point
│   │   ├── config.py          # Gemini settings
│   │   ├── services/
│   │   │   ├── embedding.py   # Gemini embeddings
│   │   │   ├── chat_service.py # Gemini chat
│   │   │   └── vector_store.py # Qdrant ops
│   │   ├── routers/
│   │   │   ├── ingest.py      # Upload endpoint
│   │   │   └── chat.py        # Chat endpoints
│   │   └── utils/
│   │       ├── parsers.py     # PDF/HTML/EPUB
│   │       └── chunking.py    # Text chunking
│   ├── requirements.txt       # Python deps (includes Gemini)
│   ├── .env.example          # Gemini API key template
│   ├── docker-compose.yml    # Qdrant setup
│   └── README.md
│
├── src/                       # Docusaurus source
│   ├── components/
│   │   └── ChatbotWidget/    # Chat popup widget
│   │       ├── index.js      # React component
│   │       └── styles.module.css
│   └── theme/
│       └── Root.js           # Global wrapper
│
├── frontend/                  # Standalone version (optional)
│   └── ...
│
└── docs/                      # Book content
    └── ...
```

---

## 🔧 Configuration

### Backend (.env file):
```env
GEMINI_API_KEY=your-key-here
QDRANT_URL=http://localhost:6333
EMBEDDING_MODEL=models/embedding-001
CHAT_MODEL=gemini-pro
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### Chatbot Widget Location:
- Har page ke bottom-right corner mein
- Purple button (💬)
- Click to open/close

---

## 💡 How It Works

### Book Upload Flow:
```
1. User uploads PDF → FastAPI receives
2. Parse PDF → Extract text
3. Chunk text → 1000 tokens each, 200 overlap
4. Generate embeddings → Gemini API (768-dim)
5. Store in Qdrant → Vector database
6. Ready for Q&A!
```

### Chat Flow:
```
1. User asks "What is ROS 2?"
2. Convert question → embedding (Gemini)
3. Search Qdrant → Top 5 similar chunks
4. Build prompt → chunks + question
5. Gemini generates answer
6. Return answer + sources
```

---

## 🎨 Chatbot Features

### Normal Chat Mode 🔍
- Searches entire book
- Shows source chunks
- Similarity scores
- Multi-turn conversation

### Selected Text Mode 📝
- Paste any text
- Ask questions about it
- No vector search
- Instant answers

---

## 🆚 Gemini vs OpenAI

| Feature | Gemini | OpenAI |
|---------|--------|--------|
| **Cost** | FREE (60 req/min) | Paid ($$$) |
| **API Key** | No credit card | Credit card required |
| **Embeddings** | 768-dim | 1536-dim |
| **Chat Model** | gemini-pro | GPT-4 |
| **Quality** | Good (~GPT-3.5) | Excellent |
| **Speed** | Fast | Fast |

**Recommendation:** Gemini for development/testing, evaluate costs for production.

---

## 🐛 Troubleshooting

### Backend Issues:

**"Module not found"**
```bash
pip install -r backend/requirements.txt
```

**"Qdrant connection refused"**
```bash
cd backend
docker-compose up -d
docker ps  # Check running
```

**"Invalid Gemini API key"**
- Check .env file
- Key sahi copy kiya hai ya nahi
- Spaces nahi hone chahiye

### Frontend Issues:

**Chat button nahi dikh raha**
```bash
# Docusaurus rebuild karo
npm run build
npm start
```

**"CORS error"**
- Backend running hai ya nahi check karo
- .env mein ALLOWED_ORIGINS check karo

### Chat Issues:

**"This information is not available"**
- Book properly upload hua ya nahi
- Question book ke scope mein hai ya nahi
- Try rephrasing question

**Slow responses**
- Normal hai (Gemini API call + Qdrant search)
- Usually 2-3 seconds

---

## 📊 Testing Checklist

- [ ] Backend health check: `curl http://localhost:8000/health`
- [ ] Qdrant running: http://localhost:6334 (dashboard)
- [ ] Frontend running: http://localhost:3000
- [ ] Chat button visible: Bottom-right corner
- [ ] Book upload works
- [ ] Normal chat works
- [ ] Selection chat works
- [ ] Sources shown correctly

---

## 🚀 Production Deployment

### Backend Options:
- Render.com (free tier)
- Railway.app
- Fly.io
- AWS/GCP/Azure

### Frontend:
- Already on Vercel/GitHub Pages
- Widget will work if backend URL is configured

### Qdrant:
- Qdrant Cloud (free tier)
- Self-hosted

---

## 💰 Cost Estimates

### Development (FREE):
- Gemini API: FREE (60 req/min)
- Qdrant: Local Docker (FREE)
- Frontend: Local (FREE)

### Production:
- Gemini: FREE tier or ~$1-5/month
- Qdrant Cloud: FREE tier or ~$25/month
- Backend hosting: ~$0-7/month (Render free tier)

**Total:** Can run completely FREE!

---

## 📚 Next Steps

1. ✅ Setup complete
2. 📖 Upload your book
3. 💬 Test questions
4. 🎨 Customize widget colors (optional)
5. 🚀 Deploy to production (optional)

---

## 🆘 Support

**Documentation:**
- Backend README: `backend/README.md`
- Gemini Setup: `backend/GEMINI-SETUP.md`
- API Docs: http://localhost:8000/docs

**Test Files:**
- Sample PDF in `backend/tests/fixtures/`
- Example questions in README

---

**Enjoy your FREE RAG chatbot powered by Google Gemini! 🎉**
