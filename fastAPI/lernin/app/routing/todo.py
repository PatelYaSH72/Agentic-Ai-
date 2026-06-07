from fastapi import APIRouter, Depends
from app.models.todo import createTodo
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.schema.todo_schema import TodoSchema
from sqlalchemy import select

router = APIRouter(prefix="/todo")



@router.get("/")
def index(db:Annotated[Session, Depends(get_db)]):
  stmt = select(TodoSchema.id, TodoSchema.content, TodoSchema.is_completed)

  todos = db.execute(stmt).mappings().all()
  # todos = db.query(TodoSchema).all()
  return {"message":"This is the TODO router", "data":todos}


@router.get("/{id}")
def show(id: int, db: Annotated[Session,Depends(get_db)]):
  todos = db.query(TodoSchema).filter(TodoSchema.id == id).first()
  return {"message":"Get a TODO item", "data":todos}


@router.post("/")
def store(item: createTodo, db:Annotated[Session, Depends(get_db)]):

  todo = TodoSchema(content=item.content, is_completed=item.is_completed)
  db.add(todo)
  db.commit()
  db.refresh(todo)


  return {"message":"Create a new TODO item","items":item.model_dump()}


@router.delete("/{id}")
def delete(id:int, db:Annotated[Session, Depends(get_db)]):
  todos = db.query(TodoSchema).filter(TodoSchema.id == id).first()

  if not todos:
    return {"Message":"Todo item not found"}
  
  db.delete(todos)
  db.commit()
  return {"Message": "TODO item deleted successfully"}


@router.put("/{id}")
def update(id: int,item:createTodo, db:Annotated[Session, Depends(get_db)]):
  todo = db.query(TodoSchema).filter(TodoSchema.id == id).first()

  if not todo:
    return {"message":"TODO item not found"}
  
  todo.content = item.content
  todo.is_completed = item.is_completed
  db.commit()
  db.refresh(todo)

  return {"Message": "TODO item updated successfully", "item":todo}