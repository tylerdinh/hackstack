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
Run this SQL in your Supabase SQL Editor to create a table for the notes.

```sql
CREATE TABLE notes (
  id SERIAL PRIMARY KEY,
  content TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 2. Backend Logic

#### `backend/app/storage/supabase_utils.py`
Add:
```python
def save_note(content: str):
    return supabase.table("notes").insert({"content": content}).execute()

def get_notes():
    return supabase.table("notes").select("*").execute()
```

#### `backend/app/main.py`
Add:
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
Change to:
```tsx
import { useEffect, useState } from 'react';
import { fetchNotes, postNote } from './api/notes';

function App() {
  const [notes, setNotes] = useState<{ id: number; content: string }[]>([]);
  const [input, setInput] = useState('');

  const loadNotes = () => fetchNotes().then(setNotes);

  useEffect(() => { loadNotes(); }, []);

  const handleSubmit = async () => {
    await postNote(input);
    setInput('');
    loadNotes();
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Simple Note Taker</h1>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={handleSubmit}>Add Note</button>
      <ul>
        {notes.map(n => <li key={n.id}>{n.content}</li>)}
      </ul>
    </div>
  );
}

export default App;
```