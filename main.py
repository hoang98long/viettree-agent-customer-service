from fastapi import FastAPI
from app.api.v1 import chat_router

app = FastAPI(title="Agentic AI")

app.include_router(chat_router, prefix="/api/v1")