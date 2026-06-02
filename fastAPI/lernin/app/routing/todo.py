from fastapi import APIRouter
from app.models.todo import createTodo

router = APIRouter(prefix="/todo")

@router.get("/")
def index():
  return {"message":"This is the TODO router"}

@router.post("/")
def store(item: createTodo):
  return {"message":"Create a new TODO item","items":item.model_dump()}