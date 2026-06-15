from fastapi import APIRouter, Depends
from app.models.blog import createBlog
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.schema.blog_schema import BlogSchema
from sqlalchemy import select

router = APIRouter(prefix="/blog")

@router.post("/")
def store(item: createBlog, db:Annotated[Session,Depends(get_db)]):

  blog = BlogSchema(title=item.title, content=item.content)

  db.add(blog)
  db.commit()
  db.refresh(blog)

  return {"message":"Create a new TODO item", "items":item.model_dump()}

@router.get("/")
def getall(db:Annotated[Session, Depends(get_db)]):

  blog = select(BlogSchema.id, BlogSchema.content, BlogSchema.title)
  
  blog = db.execute(blog).mappings().all()

  return {"message":"This is the TODO router", "data":blog }

@router.get("/{id}")
def show(id:int, db:Annotated[Session, Depends(get_db)]):
   blog = db.query(BlogSchema).filter(BlogSchema.id == id).first()
   return {"message":"Get a Blog item","data":blog}

@router.put("/{id}")
def update(id: int,item:createBlog, db:Annotated[Session, Depends(get_db)]):
  blog = db.query(BlogSchema).filter(BlogSchema.id == id).first()

  if not blog:
    return {"message":"Blog item not found"}
  
  blog.title = item.title
  blog.content = item.content
  db.commit()
  db.refresh(blog)

  return {"Message": "Blog item updated successfully", "item":blog}

@router.delete("/{id}")
def delete(id: int, db:Annotated[Session, Depends(get_db)]):
  blogs = db.query(BlogSchema).filter(BlogSchema.id == id).first()

  if not blogs:
    return {"Message":"Blog item not found"}
  
  db.delete(blogs)
  db.commit()
  return {"Message":"Blog item deleted successfully"}