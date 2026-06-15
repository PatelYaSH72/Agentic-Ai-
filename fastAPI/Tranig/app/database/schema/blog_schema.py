from sqlalchemy import Column, Integer, String, VARCHAR,Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from ..db import Base
from datetime import datetime, timezone


class BlogSchema(Base):
  __tablename__ = "blog"

  id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
  title: Mapped[str] = mapped_column(String, nullable=False)
  content:Mapped[str] = mapped_column(String, nullable=False)