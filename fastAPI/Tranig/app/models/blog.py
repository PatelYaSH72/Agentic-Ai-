from pydantic import BaseModel, Field
from typing import Optional

class createBlog(BaseModel):
  title : str = Field(..., max_length=30,min_length=2)
  content: str = Field(...,max_length=500, min_length=5)