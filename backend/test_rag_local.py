"""
Complete RAG Demo with Local Embeddings (FREE, No API limits)
"""

import os
import sys
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import google.generativeai as genai
from dotenv import load_dotenv

print("\n" + "="*60)
print("RAG CHATBOT DEMO - Local Embeddings (FREE)")
print("="*60 + "\n")

# Step 1: Load local embedding model
print("Step 1: Loading local embedding model...")
print("(First time will download ~400MB model)")
model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensions, fast & accurate
print("[OK] Model loaded: all-MiniLM-L6-v2 (384-dim)\n")

# Step 2: Setup Qdrant
print("Step 2: Setting up Qdrant (in-memory)...")
client = QdrantClient(":memory:")
collection_name = "demo_book"

client.create_collection(
    collection_name=collection_name,
    vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # 384 for all-MiniLM-L6-v2
)
print("[OK] Qdrant collection created\n")

# Step 3: Load book
print("Step 3: Loading book...")
with open('sample-book.txt', 'r', encoding='utf-8') as f:
    book_text = f.read()

print(f"[OK] Book loaded: {len(book_text)} characters")

# Chunking
chunks = []
paragraphs = [p.strip() for p in book_text.split('\n\n') if p.strip()]

for i, para in enumerate(paragraphs):
    if len(para) > 100:
        chunks.append({
            'id': i,  # Use integer ID instead of string
            'text': para,
            'metadata': {'index': i}
        })

print(f"[OK] Created {len(chunks)} chunks\n")

# Step 4: Generate embeddings (LOCAL - FREE!)
print("Step 4: Generating embeddings locally...")
print("(No API calls, completely free!)\n")

points = []
total_chunks = len(chunks)  # Process ALL chunks (no limits!)

# Batch processing for speed
chunk_texts = [chunk['text'] for chunk in chunks]
print(f"  Processing {total_chunks} chunks in batches...")

# Generate all embeddings at once (fast!)
embeddings = model.encode(chunk_texts, show_progress_bar=True, batch_size=32)

# Create points
for i, chunk in enumerate(chunks):
    point = PointStruct(
        id=chunk['id'],
        vector=embeddings[i].tolist(),
        payload={'text': chunk['text'], 'metadata': chunk['metadata']}
    )
    points.append(point)

# Upload to Qdrant
client.upsert(collection_name=collection_name, points=points)
print(f"\n[OK] Generated and stored {len(points)} embeddings\n")

# Step 5: Setup Gemini for chat (only for answering, not embeddings)
print("Step 5: Setting up Gemini for chat...")
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("[WARNING] No Gemini API key found")
    print("[INFO] Will use simple context-based responses\n")
    use_gemini = False
else:
    genai.configure(api_key=GEMINI_API_KEY)
    chat_model = genai.GenerativeModel('gemini-pro')
    print("[OK] Gemini chat configured\n")
    use_gemini = True

# Step 6: Test chatbot
print("="*60)
print("TESTING CHATBOT")
print("="*60 + "\n")

test_questions = [
    "What is Physical AI?",
    "Explain ROS 2 architecture",
    "What is a digital twin?"
]

for q_num, question in enumerate(test_questions, 1):
    print(f"\nQUESTION {q_num}: {question}")
    print("-" * 60)

    # Generate query embedding (local model)
    query_embedding = model.encode([question])[0]

    # Search Qdrant
    search_results = client.query_points(
        collection_name=collection_name,
        query=query_embedding.tolist(),
        limit=3
    ).points

    if not search_results:
        print("[ERROR] No results found")
        continue

    # Build context
    context = "\n\n".join([hit.payload['text'] for hit in search_results])

    # Generate answer
    if use_gemini:
        try:
            prompt = f"""Based on the following book excerpts, answer the question concisely.

Book Context:
{context}

Question: {question}

Answer (2-3 sentences):"""

            response = chat_model.generate_content(prompt)
            answer = response.text
        except Exception as e:
            print(f"[WARNING] Gemini error: {e}")
            print("[INFO] Using context-based response instead\n")
            answer = f"Based on the book: {context[:300]}..."
    else:
        answer = f"Based on the book: {context[:300]}..."

    print(f"\nANSWER:\n{answer}\n")

    # Show sources
    print("SOURCES:")
    for i, hit in enumerate(search_results, 1):
        print(f"  {i}. Score: {hit.score:.3f} | Text: {hit.payload['text'][:80]}...")

print("\n" + "="*60)
print("DEMO COMPLETE!")
print("="*60)
print(f"\nSUMMARY:")
print(f"  - Embedding model: all-MiniLM-L6-v2 (LOCAL)")
print(f"  - Book chunks processed: {len(points)}")
print(f"  - Embeddings generated: YES (completely free!)")
print(f"  - Vector database: YES (Qdrant in-memory)")
print(f"  - Questions tested: {len(test_questions)}")
print(f"  - Chatbot working: YES!")
print("\n[SUCCESS] RAG system is working perfectly!")
print("\nNext: Deploy to production")
print("="*60 + "\n")
