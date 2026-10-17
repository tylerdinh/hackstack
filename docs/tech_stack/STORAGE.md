# Storage

## Supabase

Data is stored in [Supabase](https://supabase.com) (hosted Postgres). All data access goes through the backend, which talks to Supabase with the Python client. The frontend only talks to Supabase directly for login (see [Authentication](#authentication)).

### Configuration
Backend credentials live in `backend/.env` and are loaded by `backend/app/core/settings.py`:

| Variable | Required | Purpose |
| --- | --- | --- |
| `SUPABASE_URL` | Yes | Your project URL (Project Settings → API). |
| `SUPABASE_SERVICE_ROLE_KEY` | Yes | Server-side key that bypasses Row Level Security. Never expose it to the frontend. |

### Access
- `backend/app/storage/supabase_utils.py` creates the client (`get_admin_client()`) and holds the functions that read and write tables.
- Services call these storage functions; routes call services.

### Tables
Create tables in the Supabase dashboard's SQL Editor. Keep the SQL for each table in your notes or `backend/app/models/` so teammates can recreate it.

## Authentication

Use [Supabase Auth](https://supabase.com/docs/guides/auth) for sign-up and login. The frontend signs users in, and the backend verifies who they are on each request:

1. **Frontend:** copy `frontend/.env.example` to `frontend/.env.local` and fill in `VITE_SUPABASE_URL` and the **anon** key `VITE_SUPABASE_ANON_KEY`, then restart `npm run dev`. `frontend/src/api/supabase.ts` creates the client; sign in with e.g. `getSupabase().auth.signInWithPassword({ email, password })`.
2. **Requests:** call the backend with `apiFetch` from `frontend/src/api/client.ts`. It attaches the logged-in user's access token automatically, sets the JSON content type, and throws on error responses:
   ```ts
   import { apiFetch } from "../api/client";

   const notes = await apiFetch<Note[]>("/api/notes");
   await apiFetch("/api/notes", { method: "POST", body: JSON.stringify({ content }) });
   ```
3. **Backend:** protect a route with the `get_current_user` dependency from `app/core/auth.py`. It returns the Supabase user, or responds `401` if the token is missing or invalid:
   ```python
   from fastapi import Depends
   from app.core.auth import get_current_user

   @router.get("/me")
   def me(user=Depends(get_current_user)):
       return {"id": user.id, "email": user.email}
   ```

Because the backend uses the service role key, Row Level Security does not apply to its queries. Filter by `user.id` yourself, e.g. `.eq("user_id", user.id)`.
