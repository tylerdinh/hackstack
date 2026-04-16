# HackStack
The best tech stack for rapid prototype development, designed to be as minimal and easy as possible.

## Tech Stack

Frontend: Vite with React (TypeScript + React Compiler), and Tailwind CSS, described specifically in docs/FRONTEND.md

Backend: FastAPI (Python), described specifically in docs/BACKEND.md

Storage: Supabase, described specifically in docs/STORAGE.md

## Build and Run

Starting from the project root: 
```
npm install 
npm run dev # The frontend/backend (concurrent!)
```

Create a .env file in the /backend folder, populate with your information:
```
SUPABASE_URL=hello.com
SUPABASE_ANON_KEY=1234
SUPABASE_SERVICE_ROLE_KEY=1234
```

## Example

Simple full-stack notetaker application, incorporating elements of the frontend/backend/storage.

### 1. Database Setup (Supabase)
Run this SQL in your Supabase SQL Editor to create a table for the notes. Also, populate the backend/.env file with your project URL and service role key.

```sql
CREATE TABLE notes (
  id SERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 2. Backend Logic

#### `backend/app/storage/supabase_utils.py`
Add to the existing:
```python
from supabase import Client

supabase: Client = get_admin_client()

def save_note(content: str):
    return supabase.table("notes").insert({"content": content}).execute()

def get_notes():
    return supabase.table("notes").select("*").execute()
```

#### `backend/app/main.py`
Add to the existing:
```python
from app.storage.supabase_utils import save_note, get_notes

@app.get("/api/notes")
async def read_notes():
    return get_notes().data

@app.post("/api/notes")
async def create_note(note: dict):
    return save_note(note["content"]).data
```

### 3. Frontend Logic

#### `frontend/src/api/notes.ts`
Add:
```typescript
const API_URL = "http://localhost:8002";

export const fetchNotes = async () => {
  const res = await fetch(`${API_URL}/api/notes`);
  return res.json();
};

export const postNote = async (content: string) => {
  const res = await fetch(`${API_URL}/api/notes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content }),
  });
  return res.json();
};
```

#### `frontend/src/App.tsx`
Copy and change the entire file to:
```tsx
import { useEffect, useState } from 'react';
import { fetchNotes, postNote } from './api/notes';

interface Note {
  id: number;
  content: string;
}

function App() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const loadNotes = () => fetchNotes().then(setNotes);

  useEffect(() => { loadNotes(); }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);
    await postNote(input);
    setInput('');
    await loadNotes();
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-slate-50 py-12 px-4 sm:px-6">
      <div className="max-w-2xl mx-auto">
        
        {/* Header */}
        <header className="mb-10">
          <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight">
            Notes
          </h1>
          <p className="mt-2 text-slate-600">
            A simple scratchpad for your thoughts.
          </p>
        </header>

        {/* Input Section */}
        <form onSubmit={handleSubmit} className="relative mb-8">
          <input 
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Write a note..."
            className="w-full p-4 pr-32 bg-white rounded-xl border border-slate-200 shadow-sm focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none transition-all"
          />
          <button 
            type="submit"
            disabled={loading || !input.trim()}
            className="absolute right-2 top-2 bottom-2 px-6 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Saving...' : 'Add'}
          </button>
        </form>

        {/* Notes List */}
        <div className="space-y-3">
          {notes.length === 0 ? (
            <div className="text-center py-12 border-2 border-dashed border-slate-200 rounded-xl">
              <p className="text-slate-400">No notes found. Create one above!</p>
            </div>
          ) : (
            notes.map((note) => (
              <div 
                key={note.id} 
                className="group p-4 bg-white rounded-xl border border-slate-200 shadow-sm hover:border-indigo-200 hover:shadow-md transition-all"
              >
                <p className="text-slate-700 leading-relaxed">
                  {note.content}
                </p>
              </div>
            ))
          )}
        </div>

        {/* Footer Info */}
        <footer className="mt-12 text-center">
          <span className="text-xs font-medium text-slate-400 uppercase tracking-widest">
            Built with HackStack
          </span>
        </footer>
      </div>
    </div>
  );
}

export default App;
```