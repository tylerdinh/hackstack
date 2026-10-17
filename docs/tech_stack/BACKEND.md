# Backend

## Dependencies

Python dependencies are managed with [uv](https://docs.astral.sh/uv/) in `backend/pyproject.toml`. Add a package with `uv add <package>` from the `backend/` folder; `uv run` installs everything automatically.

## Linting & Formatting

[Ruff](https://docs.astral.sh/ruff/) is configured in `backend/pyproject.toml`. From the project root, `npm run lint` checks the code and `npm run format` fixes and formats it.

## Serving the Frontend

In production (`npm start`), `app/main.py` serves the built frontend from `frontend/dist`: any `GET` that isn't under `/api` and doesn't match a route returns the matching static file, or `index.html` so client-side routes work. Keep every API route under `/api`. `GET /api/health` returns `{"status": "ok"}` for uptime checks, and FastAPI's interactive docs are at `/docs`.

## Source Code Folder (`backend/app/`)

### `api/`
**Route Handlers.**
- **Purpose:** Defines API endpoints and handles HTTP status codes.

### `core/`
**Configuration & Security.**
- **Purpose:** Centralizes app-wide settings, authentication logic, and environment variables.
- `settings.py` loads `backend/.env`; `auth.py` provides `get_current_user`, a route dependency that verifies Supabase access tokens (see `STORAGE.md`).

### `services/`
**Business Logic.**
- **Purpose:** Contains the core functional logic of the application, API routes should call services / services should never know they are being called by an API.

### `models/`
**Database Modeling.**
- **Purpose:** Definitions for database tables and relations.

### `schemas/`
**API Data Shapes.**
- **Purpose:** Pydantic models for request validation and response serialization.

### `storage/`
**Data Access Layer.**
- **Purpose:** Manages database connections and utility clients (e.g., Supabase client).

### `utils/`
**Helper Functions.**
- **Purpose:** Small, generic helpers (formatting, parsing, etc.) that don't belong to a specific service.
