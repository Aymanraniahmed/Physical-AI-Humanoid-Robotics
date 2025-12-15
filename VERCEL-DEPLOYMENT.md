# Vercel Deployment Guide

## ✅ Frontend (Docusaurus) - Vercel

Your Docusaurus site is ready to deploy on Vercel!

### Steps:

1. **Connect to Vercel:**
   - Go to https://vercel.com
   - Click "Add New" → "Project"
   - Import your GitHub repository: `Aymanraniahmed/Physical-AI-Humanoid-Robotics`

2. **Configure Project:**
   - Framework Preset: **Docusaurus 2**
   - Root Directory: `Physical-AI-Humanoid-Robotics-`
   - Build Command: `npm run build`
   - Output Directory: `build`

3. **Deploy:**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your site will be live at: `https://your-project.vercel.app`

### Automatic Deployments:
- Every push to `001-physical-ai-book` branch will auto-deploy! 🚀

---

## ⚠️ Backend (RAG Chatbot) - NOT Vercel

**Important:** The FastAPI backend CANNOT be deployed on Vercel because:
- Vercel has 10-second timeout (too short for RAG operations)
- Needs persistent storage for embeddings
- Requires long-running processes

### Backend Deployment Options:

### Option 1: Railway (Recommended ✅)

**Why Railway?**
- Free tier available
- Supports long-running processes
- Easy Python deployment
- Persistent storage

**Steps:**
1. Go to https://railway.app
2. Connect GitHub repo
3. Select `backend` directory
4. Add environment variables:
   ```
   GEMINI_API_KEY=your-api-key
   QDRANT_URL=:memory:
   CHAT_MODEL=models/gemini-2.5-flash
   ```
5. Deploy!

### Option 2: Render

**Steps:**
1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Root Directory: `backend`
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables (same as above)

### Option 3: Fly.io

**Steps:**
1. Install Fly CLI: `npm install -g flyctl`
2. Run in `backend` directory:
   ```bash
   fly launch
   fly secrets set GEMINI_API_KEY=your-key
   fly deploy
   ```

---

## 🔗 Connect Frontend to Backend

After deploying backend, update the chatbot widget:

**File:** `Physical-AI-Humanoid-Robotics-/src/components/ChatbotWidget/index.js`

```javascript
// Change this line:
const API_URL = 'http://localhost:8000';

// To your deployed backend URL:
const API_URL = 'https://your-backend.railway.app';  // or render.com, fly.io
```

Then commit and push:
```bash
git add .
git commit -m "Update API URL to production backend"
git push origin 001-physical-ai-book
```

Vercel will auto-deploy the updated frontend! 🎉

---

## 🚀 Complete Deployment Checklist

### Frontend (Vercel):
- [x] Code pushed to GitHub
- [ ] Connected to Vercel
- [ ] Deployed successfully
- [ ] Update API_URL when backend is ready

### Backend (Railway/Render/Fly):
- [ ] Choose deployment platform
- [ ] Deploy backend
- [ ] Add GEMINI_API_KEY environment variable
- [ ] Test API endpoints
- [ ] Update frontend API_URL

### Final Steps:
- [ ] Test chatbot on production
- [ ] Verify book content loads
- [ ] Test Q&A responses

---

## 📝 Environment Variables for Backend

Required on deployment platform:

```env
GEMINI_API_KEY=your-actual-gemini-api-key
QDRANT_URL=:memory:
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
CHAT_MODEL=models/gemini-2.5-flash
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=False
ALLOWED_ORIGINS=https://your-project.vercel.app,http://localhost:3000
```

**Important:** Update `ALLOWED_ORIGINS` with your actual Vercel URL!

---

## 🎯 Quick Deploy Commands

```bash
# Frontend is already pushed ✅

# For backend (if using Railway):
cd backend
railway login
railway init
railway up

# For backend (if using Render):
# Use web interface at render.com

# For backend (if using Fly):
cd backend
fly launch
fly deploy
```

---

## Need Help?

- Vercel Docs: https://vercel.com/docs
- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- Fly.io Docs: https://fly.io/docs

Happy deploying! 🚀
