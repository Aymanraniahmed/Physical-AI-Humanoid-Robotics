# Production Deployment Guide

## System Ready! - Local Embeddings (FREE)

Your RAG chatbot is now configured with **local embeddings** - completely free, no API limits!

### What's Working:

- **Embeddings**: sentence-transformers (all-MiniLM-L6-v2, 384-dim)
- **Vector DB**: Qdrant (in-memory or Docker)
- **Book Processing**: 34 chunks from Physical AI book
- **Search**: High accuracy (0.8+ relevance scores)
- **Chat**: Gemini Pro (optional, for better answers)

---

## Quick Start (Development)

### 1. Start Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Start Qdrant (if using Docker)
docker-compose up -d

# Start FastAPI server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Server**: http://localhost:8000
**API Docs**: http://localhost:8000/docs

### 2. Upload Book

```bash
curl -X POST -F "file=@backend/sample-book.txt" \
  http://localhost:8000/ingest/book
```

**Response**:
```json
{
  "book_id": "abc123...",
  "total_chunks": 34,
  "status": "completed"
}
```

### 3. Test Chat

```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "abc123...",
    "message": "What is Physical AI?"
  }'
```

---

## Production Deployment Options

### Option 1: Deploy to Render (Easiest)

**Step 1**: Create `render.yaml`

```yaml
services:
  - type: web
    name: rag-chatbot-backend
    env: python
    buildCommand: cd backend && pip install -r requirements.txt
    startCommand: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GEMINI_API_KEY
        value: YOUR_GEMINI_KEY
      - key: QDRANT_URL
        value: :memory:
```

**Step 2**: Push to GitHub and connect to Render

**Cost**: FREE tier available

---

### Option 2: Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and initialize
railway login
railway init

# Set environment variables
railway variables set GEMINI_API_KEY=your_key_here
railway variables set QDRANT_URL=:memory:

# Deploy
railway up
```

**Cost**: $5/month (500 hours free)

---

### Option 3: Deploy to AWS EC2

**Step 1**: Launch EC2 instance (Ubuntu 22.04, t2.micro)

**Step 2**: SSH and setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.11 python3-pip -y

# Install Docker (for Qdrant)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone your repo
git clone YOUR_REPO_URL
cd Physical-AI-Humanoid-Robotics-/backend

# Install dependencies
pip install -r requirements.txt

# Start Qdrant
docker-compose up -d

# Start backend with systemd
sudo nano /etc/systemd/system/rag-backend.service
```

**Service file**:
```ini
[Unit]
Description=RAG Chatbot Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Physical-AI-Humanoid-Robotics-/backend
ExecStart=/usr/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Start service**:
```bash
sudo systemctl daemon-reload
sudo systemctl enable rag-backend
sudo systemctl start rag-backend
```

**Cost**: ~$10/month (t2.micro)

---

### Option 4: Deploy to DigitalOcean App Platform

**Step 1**: Create `app.yaml`

```yaml
name: rag-chatbot
services:
  - name: backend
    dockerfile_path: backend/Dockerfile
    github:
      repo: YOUR_USERNAME/YOUR_REPO
      branch: main
    envs:
      - key: GEMINI_API_KEY
        value: YOUR_KEY
      - key: QDRANT_URL
        value: :memory:
    health_check:
      http_path: /health
    routes:
      - path: /
```

**Step 2**: Create `backend/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8080

# Start server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**Deploy**: Push to GitHub and connect to DigitalOcean

**Cost**: $5/month

---

## Frontend Deployment

### Deploy to Vercel (Recommended for React/Next.js)

```bash
cd Physical-AI-Humanoid-Robotics-

# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Set environment variable
vercel env add REACT_APP_API_URL production
# Enter: https://your-backend-url.com
```

**Cost**: FREE

---

### Deploy to Netlify

```bash
# Build the site
npm run build

# Deploy via Netlify CLI
npm install -g netlify-cli
netlify deploy --prod --dir=build

# Or connect GitHub repo to Netlify dashboard
```

**Cost**: FREE

---

## Environment Variables (Production)

Update these in your production environment:

```env
# Required
GEMINI_API_KEY=your_actual_gemini_key

# Qdrant Configuration
QDRANT_URL=:memory:  # For small scale
# OR
QDRANT_URL=https://your-qdrant-cloud-url  # For production scale
QDRANT_API_KEY=your_qdrant_key

# Embedding Settings
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384

# Chat Model
CHAT_MODEL=gemini-pro

# CORS (add your frontend domain)
ALLOWED_ORIGINS=https://your-frontend-domain.com,http://localhost:3000
```

---

## Scaling Considerations

### For Production Scale:

1. **Use Qdrant Cloud** instead of in-memory:
   - Sign up: https://cloud.qdrant.io
   - Create cluster (free tier: 1GB)
   - Update `QDRANT_URL` and `QDRANT_API_KEY`

2. **Add Redis** for caching:
   - Cache frequent queries
   - Store session data

3. **Use CDN** for static assets:
   - CloudFlare or AWS CloudFront
   - Faster global delivery

4. **Add monitoring**:
   - Sentry for error tracking
   - Prometheus + Grafana for metrics

---

## Cost Breakdown

### Minimal Setup (FREE):
- Embedding: Local (sentence-transformers) - $0
- Vector DB: Qdrant in-memory - $0
- Chat: Gemini free tier - $0
- Backend: Render free tier - $0
- Frontend: Vercel/Netlify - $0

**Total: $0/month** (with limitations)

### Production Setup (~$20/month):
- Embedding: Local - $0
- Vector DB: Qdrant Cloud - $0 (1GB free)
- Chat: Gemini with billing - ~$5/month
- Backend: Railway/DigitalOcean - $5-10/month
- Frontend: Vercel - $0
- Domain: Namecheap - $10/year

**Total: ~$20/month**

---

## Testing Production Deployment

```bash
# Health check
curl https://your-backend-url.com/health

# Upload book
curl -X POST -F "file=@sample-book.txt" \
  https://your-backend-url.com/ingest/book

# Test chat
curl -X POST https://your-backend-url.com/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "YOUR_BOOK_ID",
    "message": "What is Physical AI?"
  }'
```

---

## Next Steps

1. Choose deployment platform (Render recommended for beginners)
2. Set up environment variables
3. Deploy backend
4. Deploy frontend
5. Connect custom domain (optional)
6. Monitor and scale as needed

**System is ready for production!**
