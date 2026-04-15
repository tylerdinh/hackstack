from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.supabase_utils import get_admin_client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def test_functionality():
    return {"Hello": "World"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_admin_client() #On startup, try and load supabase client before everything else, ping it?
    yield