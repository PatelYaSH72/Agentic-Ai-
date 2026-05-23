from pydantic import BaseModel, field_validator
from datetime import datetime

class NoteCreate(BaseModel):
    title: str
    content: str

    @field_validator("title")
    @classmethod
    def title_valid(cls, v):
        if len(v) < 3:
            raise ValueError("Title kam se kam 3 characters ka hona chahiye")
        return v

    @field_validator("content")
    @classmethod
    def content_valid(cls, v):
        if len(v) < 10:
            raise ValueError("Content kam se kam 10 characters ka hona chahiye")
        return v

class NoteResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True