# Backend Server Ko Restart Karne Ka Tarika

## Problem
Backend server purane code ke saath chal raha hai. New changes load nahi ho rahe.

## Solution - Server ko restart karo

### Method 1: Terminal mein (Recommended)

1. **Pehle running server ko band karo:**
   - Jis terminal mein backend chal raha hai, wahan jaao
   - `Ctrl + C` press karo (server stop ho jayega)

2. **Phir server ko fresh start karo:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Method 2: Task Manager se (Windows)

Agar terminal se band nahi ho raha to:

1. `Ctrl + Shift + Esc` press karo (Task Manager khulega)
2. "Python" ya "python.exe" process dhundo
3. Right click → "End Task"
4. Phir Method 1 ke step 2 follow karo

### Method 3: PowerShell Command

```powershell
# Saare Python processes ko band karo
Get-Process python* | Stop-Process -Force

# Phir backend directory mein jaao aur start karo
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Verify Server Started Successfully

Server start hone ke baad ye output dikhna chahiye:

```
============================================================
AUTO-LOADING BOOK INTO VECTOR DATABASE
============================================================

[1/4] Loading book from sample-book.txt...
[OK] Book loaded: XXXXX characters

[2/4] Chunking text...
[OK] Created XX chunks

[3/4] Generating embeddings (local model)...
[OK] Generated XX embeddings

[4/4] Storing in vector database...
[OK] Stored XX vectors in Qdrant

============================================================
[SUCCESS] BOOK AUTO-LOADED SUCCESSFULLY!
[READY] Chatbot ready to answer questions!
============================================================
```

Agar ye message dikha to backend sahi se start ho gaya! 🎉

## Test Karo

Browser mein jaao aur chatbot ko kuch poocho:
- "What is Physical AI?"
- "Explain ROS 2 architecture"
- "What are digital twins?"

Chatbot ab book se sahi answer dega! ✅
