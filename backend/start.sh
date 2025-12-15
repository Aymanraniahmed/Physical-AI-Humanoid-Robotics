#!/bin/bash

echo "==============================================="
echo "Starting RAG Chatbot Backend (Production)"
echo "==============================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if Qdrant is running (if using Docker)
if [ "$QDRANT_URL" != ":memory:" ]; then
    echo "Checking Qdrant connection..."
    if ! docker ps | grep -q qdrant; then
        echo "Starting Qdrant with Docker Compose..."
        docker-compose up -d
    fi
fi

# Wait for Qdrant to be ready
sleep 2

# Start FastAPI server
echo ""
echo "==============================================="
echo "Starting FastAPI server..."
echo "API Docs: http://localhost:8000/docs"
echo "Health Check: http://localhost:8000/health"
echo "==============================================="
echo ""

# Run with auto-reload for development
# For production, remove --reload flag
python -m uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload
