from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.storage.supabase_utils import get_admin_client

FRONTEND_DIST = Path(__file__).parent.parent.parent / "frontend" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_admin_client()  # On startup, load the Supabase client so bad credentials fail fast
    yield


app = FastAPI(lifespan=lifespan)

# The Vite dev server proxies /api to this backend, so CORS is only needed
# when the frontend calls the backend directly (e.g. from another origin).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.exception_handler(StarletteHTTPException)
async def serve_frontend(request: Request, exc: StarletteHTTPException):
    # In production (after `npm run build`), any non-API path that no route matched
    # is served from frontend/dist, falling back to index.html for client-side routes.
    if (
        exc.status_code != 404
        or request.method != "GET"
        or request.url.path.startswith("/api")
        or not FRONTEND_DIST.exists()
    ):
        return await http_exception_handler(request, exc)

    file = (FRONTEND_DIST / request.url.path.lstrip("/")).resolve()
    if file.is_file() and file.is_relative_to(FRONTEND_DIST.resolve()):
        return FileResponse(file)
    return FileResponse(FRONTEND_DIST / "index.html")
