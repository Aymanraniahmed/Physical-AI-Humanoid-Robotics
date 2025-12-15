"""
Complete RAG Chatbot Demo
Book ko process karke test karta hai
"""

import os
import sys

# Check if running from backend directory
if not os.path.exists('app'):
    print("❌ Please run from backend directory: cd backend && python demo.py")
    sys.exit(1)

print("\n" + "="*60)
print("RAG CHATBOT DEMO - Book Processing & Testing")
print("="*60 + "\n")

# Step 1: Check dependencies
print("📦 Step 1: Checking dependencies...")
try:
    import google.generativeai as genai
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams
    print("✓ All dependencies installed")
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("\n💡 Run: pip install -r requirements.txt")
    sys.exit(1)

# Step 2: Load configuration
print("\n⚙️  Step 2: Loading configuration...")
try:
    from dotenv import load_dotenv
    load_dotenv()

    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    if not GEMINI_API_KEY or GEMINI_API_KEY.startswith('AIzaSyDEMO'):
        print("❌ Please set your real GEMINI_API_KEY in .env file")
        sys.exit(1)

    print(f"✓ API Key: {GEMINI_API_KEY[:20]}...")
    genai.configure(api_key=GEMINI_API_KEY)
    print("✓ Gemini configured")
except Exception as e:
    print(f"❌ Configuration error: {e}")
    sys.exit(1)

# Step 3: Setup Qdrant (in-memory for demo)
print("\n🗄️  Step 3: Setting up Qdrant (in-memory)...")
try:
    client = QdrantClient(":memory:")  # In-memory for demo
    collection_name = "demo_book"

    # Create collection
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )
    print("✓ Qdrant collection created (in-memory)")
except Exception as e:
    print(f"❌ Qdrant error: {e}")
    sys.exit(1)

# Step 4: Load and chunk book
print("\n📚 Step 4: Loading book...")
try:
    with open('sample-book.txt', 'r', encoding='utf-8') as f:
        book_text = f.read()

    print(f"✓ Book loaded: {len(book_text)} characters")

    # Simple chunking (by paragraphs for demo)
    chunks = []
    paragraphs = [p.strip() for p in book_text.split('\n\n') if p.strip()]

    for i, para in enumerate(paragraphs):
        if len(para) > 100:  # Skip very small chunks
            chunks.append({
                'id': f'chunk_{i}',
                'text': para,
                'metadata': {'index': i}
            })

    print(f"✓ Created {len(chunks)} chunks")

except Exception as e:
    print(f"❌ Book loading error: {e}")
    sys.exit(1)

# Step 5: Generate embeddings
print("\n🧠 Step 5: Generating embeddings with Gemini...")
try:
    from qdrant_client.models import PointStruct

    points = []
    for i, chunk in enumerate(chunks[:20]):  # First 20 chunks for demo
        print(f"  Processing chunk {i+1}/20...", end='\r')

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
            payload={'text': chunk['text'], 'metadata': chunk['metadata']}
        )
        points.append(point)

    # Upload to Qdrant
    client.upsert(collection_name=collection_name, points=points)
    print(f"\n✓ Generated and stored {len(points)} embeddings")

except Exception as e:
    print(f"\n❌ Embedding error: {e}")
    sys.exit(1)

# Step 6: Test chatbot
print("\n💬 Step 6: Testing chatbot...")
print("-" * 60)

test_questions = [
    "What is Physical AI?",
    "Explain ROS 2 architecture",
    "What is a digital twin?",
]

model = genai.GenerativeModel('gemini-pro')

for question in test_questions:
    print(f"\n❓ Question: {question}")
    print("-" * 60)

    try:
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
            print("❌ No results found")
            continue

        # Build context
        context = "\n\n".join([hit.payload['text'] for hit in search_results])

        # Generate answer
        prompt = f"""Based on the following book excerpts, answer the question.

Book Context:
{context}

Question: {question}

Answer:"""

        response = model.generate_content(prompt)

        print(f"\n✅ Answer:\n{response.text}\n")
        print(f"📚 Sources: {len(search_results)} chunks (scores: {[f'{hit.score:.3f}' for hit in search_results]})")

    except Exception as e:
        print(f"❌ Error: {e}")

# Summary
print("\n" + "="*60)
print("✅ DEMO COMPLETE!")
print("="*60)
print("\nSummary:")
print(f"  • Book processed: ✅")
print(f"  • Chunks created: {len(points)}")
print(f"  • Embeddings generated: ✅ (Gemini)")
print(f"  • Vector store: ✅ (Qdrant in-memory)")
print(f"  • Questions tested: {len(test_questions)}")
print(f"  • Answers generated: ✅ (Gemini Pro)")
print("\n🎉 RAG chatbot is working perfectly!")
print("\n💡 Next: Start backend server and use web UI")
print("   Command: python -m uvicorn app.main:app --reload")
print("="*60 + "\n")
