from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
  name: str
  age: int
  is_active: bool

@app.post("/register")
def home(user : User):
  return {
    "message":f"Welcome {user.name}!",
    "age":user.age,
    "active":user.is_active
  }