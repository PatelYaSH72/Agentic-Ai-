from pydantic import BaseModel
from typing import List

class Message(BaseModel):
  role:str
  content:str

class ChatRequest(BaseModel):
  message:str
  history:List[Message] | None


class ChatResponse(BaseModel):
  reply: str