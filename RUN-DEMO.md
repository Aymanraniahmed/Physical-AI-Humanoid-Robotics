# 🚀 Book Processing & Testing Demo

## IMPORTANT: Pehle Ye Karo! (2 minutes)

### Step 1: Gemini API Key Lo

1. **Browser mein jao:**
   ```
   https://makersuite.google.com/app/apikey
   ```

2. **"Create API Key" click karo**

3. **Key copy karo**

4. **backend/.env file edit karo:**
   ```env
   GEMINI_API_KEY=your-actual-key-paste-here
   ```

   Replace `AIzaSyB2307JFb04ELjudbQuU0rstTx8FunX2BE` with your real key!

---

## Ab Demo Chalao (Automatic)

Main ne **complete book** bana di hai: `backend/sample-book.txt`

Ab ye commands run karo:

### Terminal 1: Start Backend + Qdrant

```bash
cd backend

# 1. Qdrant start karo
docker-compose up -d

# 2. Dependencies install karo (agar nahi kiye)
pip install -r requirements.txt

# 3. Backend start karo
python -m uvicorn app.main:app --reload
```

**Wait for:** `Application startup complete`

---

### Terminal 2: Book Upload Karo

```bash
cd backend

# Book upload command
curl -X POST -F "file=@sample-book.txt" \
  http://localhost:8000/ingest/book
```

**Ye hoga:**
- ✅ Text parse hoga
- ✅ Chunks banenge (~15-20 chunks)
- ✅ Gemini embeddings generate hongi
- ✅ Qdrant mein store hoga
- ✅ Book ID milega

**Time:** 30-60 seconds

---

### Terminal 3: Test Questions

```bash
# Question 1: What is Physical AI?
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "PASTE_BOOK_ID_HERE",
    "message": "What is Physical AI?"
  }'

# Question 2: Explain ROS 2
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "PASTE_BOOK_ID_HERE",
    "message": "What is ROS 2 architecture?"
  }'

# Question 3: Digital Twin
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "PASTE_BOOK_ID_HERE",
    "message": "Explain digital twin"
  }'
```

---

## Ya Frontend Se Test Karo (Easy!)

### Terminal 1: Backend (same as above)
```bash
cd backend
docker-compose up -d
python -m uvicorn app.main:app --reload
```

### Terminal 2: Website
```bash
cd Physical-AI-Humanoid-Robotics-
npm start
```

### Browser:
1. Jao: http://localhost:3000
2. Bottom-right: **Purple chat button (💬)** click karo
3. **"Choose File"** → `backend/sample-book.txt` select karo
4. **Upload** karo (wait 30-60 sec)
5. **Questions poocho!**

**Example Questions:**
- "What is Physical AI?"
- "Explain ROS 2"
- "What is Isaac Sim?"
- "Tell me about humanoid robots"

---

## Expected Output

### Upload Response:
```json
{
  "book_id": "abc123-xyz...",
  "title": "sample-book.txt",
  "total_chunks": 18,
  "status": "completed",
  "message": "Successfully ingested 18 chunks"
}
```

### Chat Response:
```json
{
  "session_id": "session-123...",
  "response": "Physical AI represents a paradigm shift from traditional AI systems to intelligent systems that perceive, reason about, and interact with the physical world...",
  "sources": [
    {
      "chunk_id": "chunk-1",
      "text": "Physical AI represents...",
      "score": 0.92,
      "metadata": {...}
    }
  ]
}
```

---

## Troubleshooting

### "Invalid API key"
```bash
# .env file check karo
cd backend
cat .env | grep GEMINI_API_KEY

# Sahi key daalo (no spaces, no quotes)
GEMINI_API_KEY=AIzaSy...your-real-key...
```

### "Qdrant connection error"
```bash
# Qdrant start karo
cd backend
docker-compose up -d

# Check running hai ya nahi
docker ps | grep qdrant
```

### "Module not found"
```bash
# Dependencies install karo
cd backend
pip install -r requirements.txt
```

---

## ✅ Success Checklist

- [ ] Gemini API key set in .env
- [ ] Qdrant running (docker ps)
- [ ] Backend running (http://localhost:8000/health)
- [ ] Book uploaded successfully
- [ ] Questions get correct answers
- [ ] Sources shown with scores

---

**Book ready hai! Ab Gemini API key daalo aur demo chalao! 🚀**
