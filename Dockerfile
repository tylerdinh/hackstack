# The anon key is public by design (it ships in the browser bundle), so it's fine as a build arg
# check=skip=SecretsUsedInArgOrEnv

# Build the frontend
FROM node:22-slim AS frontend
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
# Vite bakes these into the bundle, so they're needed at build time (only if the frontend uses Supabase).
# Render and Railway pass your environment variables in as build args.
ARG VITE_SUPABASE_URL
ARG VITE_SUPABASE_ANON_KEY
RUN npm run build

# Serve the API and the built frontend from one port
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.0 /uv /usr/local/bin/uv
WORKDIR /app/backend
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --locked --no-dev
COPY backend/ ./
COPY --from=frontend /app/frontend/dist /app/frontend/dist
CMD ["sh", "-c", "uv run --no-sync fastapi run app/main.py --port ${PORT:-8002}"]
