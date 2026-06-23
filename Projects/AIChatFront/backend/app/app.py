from fastapi import FastAPI
from dotenv import load_dotenv
# from router.llmrouter import llmrouter
from app.router.llmrouter import llmrouter

app = FastAPI()

app.include_router(llmrouter)

@app.get("/")
def root():
  return {"messsage":"AI Chatbot Backend"}