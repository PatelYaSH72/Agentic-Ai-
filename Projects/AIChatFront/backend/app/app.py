from fastapi import FastAPI
from dotenv import load_dotenv
# from router.llmrouter import llmrouter
from app.router.llmrouter import llmrouter
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(llmrouter)

@app.get("/")
def root():
  return {"messsage":"AI Chatbot Backend"}