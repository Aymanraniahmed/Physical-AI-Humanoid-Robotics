# 🚀 RAG Chatbot - Quick Start Guide (Roman Urdu)

## Sirf 5 Minutes Mein Start Karo!

### ✅ Prerequisites Check Karo

```bash
# Python check karo
python --version  # 3.11+ chahiye

# Docker check karo
docker --version  # Qdrant ke liye
```

### 📦 Step 1: Setup Karo (2 minutes)

```bash
# 1. Backend folder mein jao
cd backend

# 2. Dependencies install karo
pip install -r requirements.txt

# 3. Environment file banao
copy .env.example .env  # Windows
# ya
cp .env.example .env    # Linux/Mac

# 4. .env file mein OpenAI API key daalo
# OPENAI_API_KEY=sk-your-key-here
```

### 🐳 Step 2: Qdrant Start Karo (30 seconds)

```bash
# Docker Compose se Qdrant start karo
docker-compose up -d

# Check karo running hai ya nahi
docker ps
```

### 🚀 Step 3: Backend Start Karo (10 seconds)

```bash
# Backend server start karo
python -m uvicorn app.main:app --reload
```

**✓ Success:** http://localhost:8000/docs par jao - Swagger UI dikhe!

### 🌐 Step 4: Frontend Start Karo (10 seconds)

Naya terminal kholo:

```bash
# Frontend folder mein jao
cd ../frontend

# HTTP server start karo
python -m http.server 3000
```

**✓ Success:** http://localhost:3000 par jao - UI dikhe!

### 🎯 Step 5: Use Karo!

1. **Book Upload:**
   - Click "Choose File"
   - Apni PDF/HTML/EPUB book select karo
   - Click "Upload Book"
   - Wait karo (1-2 minutes for processing)

2. **Ask Questions:**
   - Type karo: "What is Physical AI?"
   - Enter dabao
   - Answer milega with sources!

## 🎉 Done! Aap Ab RAG Chatbot Use Kar Sakte Ho!

---

## 🔧 Quick Troubleshooting

**Problem:** Qdrant connection error
```bash
# Solution:
docker-compose up -d
```

**Problem:** OpenAI API error
```bash
# Solution: .env file mein API key check karo
```

**Problem:** Module not found
```bash
# Solution:
pip install -r requirements.txt
```

---

**Full Documentation:** [README.md](backend/README.md) dekho
