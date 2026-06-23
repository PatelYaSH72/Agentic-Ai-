import os 
from groq import Groq
from schema.llmrouterSchema import Message
from typing import List

client = Groq(api_key=os.getenv("CHAT_API_KEY"))

async def get_ai_reply(message: str, history: List[Message]) -> str:

  system_prompt = {
    "role":"system",
    "content": (
            "Tum ek helpful AI assistant ho. "
            "Clearly aur concisely jawab do. "
            "Agar kuch pata nahi to honestly bolo."
        ),
  }

  conversation = []
  for msg in history:
      conversation.append({
         "role":"assistant" if msg.role == "ai" else "user",
         "content":msg.content
      })

      conversation.append({
         "role":"user",
         "content":message
      })

      response = await client.chat.completions.create(
         model=""


      )