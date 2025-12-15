# Google Gemini API Setup Guide

## ✅ Backend ab Google Gemini use karta hai! (FREE!)

OpenAI ki jagah ab Google Gemini API use ho raha hai. Gemini **FREE** hai aur powerful bhi!

## 🔑 Step 1: Gemini API Key Kaise Len

1. **Google AI Studio** par jao:
   ```
   https://makersuite.google.com/app/apikey
   ```

2. **"Create API Key"** click karo

3. **API key copy** karo

4. **`.env` file mein paste** karo:
   ```bash
   cd backend
   copy .env.example .env  # Windows
   # ya
   cp .env.example .env    # Linux/Mac
   ```

5. **.env file** edit karo:
   ```env
   GEMINI_API_KEY=your-actual-gemini-api-key-here
   ```

## 🆚 Gemini vs OpenAI

### Gemini Advantages:
✅ **FREE** (60 requests per minute free tier)
✅ **No credit card** required
✅ **Good quality** responses
✅ **768-dim embeddings** (smaller but effective)
✅ **Fast** response times

### OpenAI:
💰 Paid (needs credit card)
💰 Costly ($0.03 per 1K tokens for GPT-4)
✅ Slightly better quality
✅ 1536-dim embeddings

## 📊 What Changed?

### Before (OpenAI):
- **Embedding**: text-embedding-3-small (1536 dimensions)
- **Chat**: GPT-4 ($$$)
- **Cost**: ~$0.50 for testing

### Now (Gemini):
- **Embedding**: models/embedding-001 (768 dimensions)
- **Chat**: gemini-pro (FREE!)
- **Cost**: $0 (FREE tier)

## 🚀 How to Run

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

**New dependency:** `google-generativeai`

### 2. Setup Environment
```bash
# .env file mein daalo:
GEMINI_API_KEY=your-key-here
EMBEDDING_DIMENSION=768  # Gemini uses 768, not 1536
```

### 3. Start Qdrant
```bash
docker-compose up -d
```

### 4. Start Backend
```bash
python -m uvicorn app.main:app --reload
```

### 5. Test
```bash
# Health check
curl http://localhost:8000/health

# Upload book (same as before)
curl -X POST -F "file=@yourbook.pdf" http://localhost:8000/ingest/book
```

## 🔄 API Changes

### Services Updated:
1. **app/config.py** - Gemini settings
2. **app/services/embedding.py** - Gemini embeddings
3. **app/services/chat_service.py** - Gemini chat
4. **requirements.txt** - Added google-generativeai

### What Works Same:
- All API endpoints (same routes)
- Frontend integration (no changes needed)
- Qdrant operations (same)
- Document parsing (same)

## 📝 Example Code

### Gemini Embedding:
```python
import google.generativeai as genai

genai.configure(api_key="your-key")
result = genai.embed_content(
    model="models/embedding-001",
    content="What is Physical AI?",
    task_type="retrieval_query"
)
embedding = result['embedding']  # 768 dimensions
```

### Gemini Chat:
```python
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Answer this question...")
answer = response.text
```

## 🎯 Migration Checklist

- [x] Update config.py with Gemini settings
- [x] Update embedding.py to use Gemini API
- [x] Update chat_service.py to use Gemini models
- [x] Update requirements.txt
- [x] Update .env.example
- [x] Update vector_store dimension (768)
- [x] Test with sample book

## ⚡ Quick Start

```bash
# 1. Get API key
https://makersuite.google.com/app/apikey

# 2. Setup
cd backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add GEMINI_API_KEY

# 3. Run
docker-compose up -d
python -m uvicorn app.main:app --reload

# 4. Upload book via frontend
http://localhost:3000
```

## 💡 Tips

1. **Free Tier Limits:**
   - 60 requests per minute
   - Good for testing and small projects

2. **Rate Limiting:**
   - If you hit limits, add delays between requests
   - Or upgrade to paid tier

3. **Quality:**
   - Gemini Pro is comparable to GPT-3.5
   - For best quality, use gemini-pro-vision for images

4. **Cost Saving:**
   - Development: Use Gemini (FREE)
   - Production: Evaluate if you need GPT-4

## 🆘 Troubleshooting

**Error: "API key not valid"**
- Check key is correct in .env
- Make sure no extra spaces

**Error: "Quota exceeded"**
- You hit free tier limit (60/min)
- Wait 1 minute or upgrade

**Error: "Embedding dimension mismatch"**
- Delete old Qdrant collection
- Restart with EMBEDDING_DIMENSION=768

---

**Gemini ab FREE mein powerful RAG chatbot bana sakta hai! 🚀**
