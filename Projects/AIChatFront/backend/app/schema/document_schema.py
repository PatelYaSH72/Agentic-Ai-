from pydantic import BaseModel

class DocumentRequest(BaseModel):
  content:str

class UserQuery(BaseModel):
  query:str