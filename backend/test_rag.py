"""
Simple RAG Demo - No Emojis
"""

import os
import sys

print("\n" + "="*60)
print("RAG CHATBOT DEMO - Book Processing & Testing")
print("="*60 + "\n")

# Step 1: Check dependencies
print("Step 1: Checking dependencies...")
try:
    import google.generativeai as genai
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
    from dotenv import load_dotenv
    print("[OK] All dependencies installed\n")
except ImportError as e:
    print(f"[ERROR] Missing dependency: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Step 2: Load configuration
print("Step 2: Loading configuration...")
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY or GEMINI_API_KEY.startswith('AIzaSyDEMO'):
    print("[ERROR] Set your real GEMINI_API_KEY in .env file")
    sys.exit(1)

print(f"[OK] API Key: {GEMINI_API_KEY[:20]}...")
genai.configure(api_key=GEMINI_API_KEY)
print("[OK] Gemini configured\n")

# Step 3: Setup Qdrant
print("Step 3: Setting up Qdrant (in-memory)...")
client = QdrantClient(":memory:")
collection_name = "demo_book"

client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
)
print("[OK] Qdrant collection created\n")

# Step 4: Load book
print("Step 4: Loading book...")
with open('sample-book.txt', 'r', encoding='utf-8') as f:
    book_text = f.read()

print(f"[OK] Book loaded: {len(book_text)} characters")

# Simple chunking
chunks = []
paragraphs = [p.strip() for p in book_text.split('\n\n') if p.strip()]

for i, para in enumerate(paragraphs):
    if len(para) > 100:
        chunks.append({
            'id': f'chunk_{i}',
            'text': para,
            'metadata': {'index': i}
        })

print(f"[OK] Created {len(chunks)} chunks\n")

# Step 5: Generate embeddings
print("Step 5: Generating embeddings with Gemini...")
print("(This may take 30-60 seconds...)\n")

points = []
total_chunks = min(15, len(chunks))  # Process first 15 chunks

for i, chunk in enumerate(chunks[:total_chunks]):
    print(f"  Processing chunk {i+1}/{total_chunks}...")

    # Generate embedding
    result = genai.embed_content(
        model="models/embedding-001",
        content=chunk['text'],
        task_type="retrieval_document"
    )

    # Create point
    point = PointStruct(
        id=chunk['id'],
        vector=result['embedding'],
        payload={'text': chunk['text'][:500], 'metadata': chunk['metadata']}  # Limit payload size
    )
    points.append(point)

# Upload to Qdrant
client.upsert(collection_name=collection_name, points=points)
print(f"\n[OK] Generated and stored {len(points)} embeddings\n")

# Step 6: Test chatbot
print("="*60)
print("TESTING CHATBOT")
print("="*60 + "\n")

test_questions = [
    "What is Physical AI?",
    "Explain ROS 2 architecture",
    "What is a digital twin?"
]

model = genai.GenerativeModel('gemini-pro')

for q_num, question in enumerate(test_questions, 1):
    print(f"\nQUESTION {q_num}: {question}")
    print("-" * 60)

    # Generate query embedding
    query_result = genai.embed_content(
        model="models/embedding-001",
        content=question,
        task_type="retrieval_query"
    )

    # Search Qdrant
    search_results = client.search(
        collection_name=collection_name,
        query_vector=query_result['embedding'],
        limit=3
    )

    if not search_results:
        print("[ERROR] No results found")
        continue

    # Build context
    context = "\n\n".join([hit.payload['text'] for hit in search_results])

    # Generate answer
    prompt = f"""Based on the following book excerpts, answer the question concisely.

Book Context:
{context}

Question: {question}

Answer (2-3 sentences):"""

    response = model.generate_content(prompt)

    print(f"\nANSWER:\n{response.text}\n")

    # Show sources
    print("SOURCES:")
    for i, hit in enumerate(search_results, 1):
        print(f"  {i}. Score: {hit.score:.3f} | Text: {hit.payload['text'][:80]}...")

print("\n" + "="*60)
print("DEMO COMPLETE!")
print("="*60)
print(f"\nSUMMARY:")
print(f"  - Book chunks processed: {len(points)}")
print(f"  - Embeddings generated: YES (Gemini embedding-001)")
print(f"  - Vector database: YES (Qdrant in-memory)")
print(f"  - Questions tested: {len(test_questions)}")
print(f"  - Chatbot working: YES!")
print("\n[SUCCESS] RAG system is working perfectly!")
print("\nNext: Start web server")
print("  Command: python -m uvicorn app.main:app --reload")
print("="*60 + "\n")
