# HackStack
The best tech stack for rapid prototype development.

## Tech Stack

Frontend: Vite with React (TypeScript + React Compiler), and Tailwind CSS, described specifically in [docs/tech_stack/FRONTEND.md](docs/tech_stack/FRONTEND.md)

Backend: FastAPI (Python, dependencies managed with [uv](https://docs.astral.sh/uv/)), described specifically in [docs/tech_stack/BACKEND.md](docs/tech_stack/BACKEND.md)

Storage: Supabase, described specifically in [docs/tech_stack/STORAGE.md](docs/tech_stack/STORAGE.md)

## Build and Run

Prerequisites: [Node.js](https://nodejs.org) 22.12+ (`nvm use` picks it up from `.nvmrc`) and [uv](https://docs.astral.sh/uv/getting-started/installation/) (uv installs the pinned Python version from `backend/.python-version` for you).

Copy `backend/.env.example` to `backend/.env` and fill in your Supabase credentials (Project Settings → API):
```
cp backend/.env.example backend/.env
```

Starting from the project root:
```
npm run setup # Install frontend and backend dependencies
npm run dev   # The frontend/backend (concurrent!)
```

The frontend runs at http://localhost:8001 and the backend at http://localhost:8002 (check http://localhost:8002/api/health, and http://localhost:8002/docs for interactive API docs). To add a Python dependency, run `uv add <package>` from the `backend/` folder.

### Scripts (run from the project root)

| Command | What it does |
| --- | --- |
| `npm run setup` | Installs all Node and Python dependencies. |
| `npm run dev` | Runs the frontend and backend with hot reload. |
| `npm run frontend` / `npm run backend` | Runs just one side. |
| `npm run build` | Type-checks and builds the frontend into `frontend/dist` (`npm start` runs this for you). |
| `npm run lint` | Lints the frontend (ESLint) and backend (Ruff). |
| `npm run format` | Auto-fixes and formats backend code with Ruff. |
| `npm start` | Production: builds the frontend and serves everything from the backend at http://localhost:8002 (or `$PORT`). |

### Deploying

In production, FastAPI serves the built frontend alongside the API from a single port, so there's no CORS or proxy setup. The included `Dockerfile` packages both, so any host that runs Docker works. On [Render](https://render.com):

1. Push the repo to GitHub, then in Render choose **New → Web Service** and pick the repo. Render detects the `Dockerfile`.
2. Under **Environment**, add `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`. If the frontend uses login, also add `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` (Render passes these into the build).
3. Deploy. Render sets `PORT` and gives you a public URL; every push to `main` redeploys.

[Railway](https://railway.com) and [Fly.io](https://fly.io) work the same way: point them at the repo and set the same variables. Don't upload `.env` files; set the variables in the host's dashboard.

To try the production setup locally, run `npm start`, or with Docker:
```
docker build -t hackstack . && docker run -p 8002:8002 --env-file backend/.env hackstack
```

## Example

Simple full-stack notetaker application, incorporating elements of the frontend/backend/storage. Requests flow `api/` (routes) → `services/` (logic) → `storage/` (database).

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

After pasting, run `npm run format` from the root to tidy up spacing and import order.

#### `backend/app/storage/supabase_utils.py`
Add to the bottom of the file:
```python
supabase = get_admin_client()


def save_note(content: str):
    return supabase.table("notes").insert({"content": content}).execute().data


def get_notes():
    return supabase.table("notes").select("*").order("created_at").execute().data
```

#### `backend/app/schemas/note.py`
Add:
```python
from pydantic import BaseModel


class NoteCreate(BaseModel):
    content: str
```

#### `backend/app/services/notes.py`
Add:
```python
from app.storage.supabase_utils import get_notes, save_note


def list_notes():
    return get_notes()


def create_note(content: str):
    return save_note(content.strip())
```

#### `backend/app/api/notes.py`
Add:
```python
from fastapi import APIRouter

from app.schemas.note import NoteCreate
from app.services import notes

router = APIRouter(prefix="/api/notes")


@router.get("")
def read_notes():
    return notes.list_notes()


@router.post("")
def create_note(note: NoteCreate):
    return notes.create_note(note.content)
```

#### `backend/app/main.py`
Add the import with the other imports at the top of the file:
```python
from app.api.notes import router as notes_router
```
Then register the router below the `/api/health` route:
```python
app.include_router(notes_router)
```

### 3. Frontend Logic

#### `frontend/src/api/notes.ts`
Add (relative URLs work because Vite proxies `/api` to the backend):
```typescript
export const fetchNotes = async () => {
  const res = await fetch("/api/notes");
  if (!res.ok) throw new Error(`Failed to load notes (${res.status})`);
  return res.json();
};

export const postNote = async (content: string) => {
  const res = await fetch("/api/notes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content }),
  });
  if (!res.ok) throw new Error(`Failed to save note (${res.status})`);
  return res.json();
};
```

#### `frontend/src/pages/NotesPage.tsx`
Add:
```tsx
import { useEffect, useState } from 'react';
import { fetchNotes, postNote } from '../api/notes';

interface Note {
  id: number;
  content: string;
}

function NotesPage() {
  const [notes, setNotes] = useState<Note[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadNotes = () =>
    fetchNotes()
      .then(setNotes)
      .catch((e: Error) => setError(e.message));

  useEffect(() => { loadNotes(); }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    setLoading(true);
    setError(null);
    try {
      await postNote(input);
      setInput('');
      await loadNotes();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setLoading(false);
    }
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

        {/* Error Message */}
        {error && (
          <p className="mb-6 p-3 rounded-lg bg-red-50 border border-red-200 text-sm text-red-700">
            {error}
          </p>
        )}

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

export default NotesPage;
```

#### `frontend/src/App.tsx`
Add the import at the top of the file:
```tsx
import NotesPage from './pages/NotesPage'
```
Then add the route inside `<Routes>`, above the `"*"` route, and visit http://localhost:8001/notes:
```tsx
<Route path="/notes" element={<NotesPage />} />
```
