from fastapi import APIRouter, Depends
from app.models.auth import Register
from sqlalchemy.orm import Session
from app.database.db import get_db
from typing import Annotated
from app.database.schema.user_schema import UserSchema

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(data:Register, db:Annotated[Session, Depends(get_db)]):

# Check if user with the same email already exists
  existing_user = db.query(UserSchema).filter(UserSchema.email = data.email).first()

  if existing_user:
    return {"message": "User with this email already exists"}
