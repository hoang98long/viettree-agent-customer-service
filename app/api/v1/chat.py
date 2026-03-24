from fastapi import APIRouter

from app.schemas import ChatRequest, ChatResponse
from app.services import ask_agent

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    return ChatResponse(answer=ask_agent(req.question))