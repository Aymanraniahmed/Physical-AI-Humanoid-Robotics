# Quick Start - Chatbot Ready!

## System Status: READY!

Backend running at: **http://localhost:8000**

- Book: AUTO-LOADED (34 chunks)
- Embeddings: LOCAL (free, no API limits)
- Chat Model: Gemini Pro
- No upload needed - just ask questions!

---

## How to Use:

### 1. Backend Already Running
Backend is running at http://localhost:8000

To restart if needed:
```bash
cd backend
python -m uvicorn app.main:app --reload
```

### 2. Start Frontend (Website)
```bash
cd Physical-AI-Humanoid-Robotics-
npm start
```

Website will open at: http://localhost:3000

### 3. Use Chatbot

1. Website ke bottom-right corner mein **purple chat button** (💬) dikhega
2. Click karo
3. Seedha sawal poocho - **NO UPLOAD NEEDED!**

**Example Questions:**
- "What is Physical AI?"
- "Explain ROS 2 architecture"
- "What is Isaac Sim?"
- "Tell me about humanoid robots"
- "How does digital twin work?"

---

## What Changed:

### Before (Old System):
- User ko book upload karni padti thi
- Gemini API quota issues
- Har user ko file select karni thi

### Now (New System):
- ✅ Book automatically loaded on startup
- ✅ No upload needed
- ✅ Local embeddings (FREE, no API limits)
- ✅ Seedha chatbot ready hai
- ✅ Just open and ask!

---

## Test Commands (Optional):

```bash
# Health check
curl http://localhost:8000/health

# Direct chat test
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is Physical AI?"
  }'
```

---

## Troubleshooting:

**Backend nahi chal raha?**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Frontend nahi chal raha?**
```bash
npm install
npm start
```

**Chatbot button nahi dikh raha?**
- Page refresh karo (Ctrl+R)
- Bottom-right corner check karo

---

**Ready to use! Open website aur seedha sawal poocho!** 🚀
