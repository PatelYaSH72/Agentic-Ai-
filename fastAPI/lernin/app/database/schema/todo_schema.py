from sqlalchemy import Column, Integer, String, VARCHAR,Boolean, DateTime
from ..db import Base
from datetime import datetime, timezone

class TodoSchema(Base):
  __tablename__ = "todos"

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  content = Column(String, nullable=False)
  is_completed = Column(Boolean, default=False, nullable=False)
  create_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
  update_at = Column(DateTime, nullable=True, onupdate=datetime.now(timezone.utc))