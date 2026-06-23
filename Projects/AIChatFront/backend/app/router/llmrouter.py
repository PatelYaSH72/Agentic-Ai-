from fastapi import APIRouter, Depends, HTTPException
from app.schema.llmrouterSchema import ChatResponse, ChatRequest
from app.services.llmServices import get_ai_reply

llmrouter = APIRouter(prefix="/llm")

@llmrouter.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
  

  try:
    reply = await get_ai_reply(
           message=req.message,
           history=req.history
    )

    return ChatResponse(reply=reply)
  
  except Exception as e:
        # Kuch bhi galat ho to 500 error bhejo
        raise HTTPException(status_code=500, detail=str(e))