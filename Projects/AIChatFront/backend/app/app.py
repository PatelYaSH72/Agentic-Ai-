from fastapi import FastAPI
from dotenv import load_dotenv
# from router.llmrouter import llmrouter
from app.router.llmrouter import llmrouter
from app.router.document_route import rag_chunkrouter
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine
from app.db.models import Base

load_dotenv()

app = FastAPI()
Base.metadata.create_all(bind=engine)

print("Tables created successfully")

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(llmrouter)
app.include_router(rag_chunkrouter)

@app.get("/")
def root():
  return {"messsage":"AI Chatbot Backend"}