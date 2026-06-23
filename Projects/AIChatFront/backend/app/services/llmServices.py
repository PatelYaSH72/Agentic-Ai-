import os 
from groq import AsyncGroq
from app.schema.llmrouterSchema import Message
from typing import List
from dotenv import load_dotenv

load_dotenv()

client = AsyncGroq(api_key=os.getenv("CHAT_API_KEY"))

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
         model="llama-3.3-70b-versatile",
         messages=[system_prompt] + conversation,
         temperature=0.7,
         max_tokens=1000,


      )

  return response.choices[0].message.content