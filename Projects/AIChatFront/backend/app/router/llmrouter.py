from fastapi import APIRouter, Depends
from schema.llmrouterSchema import ChatResponse, ChatRequest

router = APIRouter(prefix="/llm")

@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
  