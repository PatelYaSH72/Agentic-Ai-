from sqlalchemy import Column, Integer, String, VARCHAR,Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from ..db import Base
from datetime import datetime, timezone

class TodoSchema(Base):
  __tablename__ = "todos"

  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
  content: Mapped[str] = mapped_column(String, nullable=False)
  is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
  create_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now(timezone.utc))
  update_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, onupdate=datetime.now(timezone.utc))