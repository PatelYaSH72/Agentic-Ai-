from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    collection_id: Mapped[int | None] = mapped_column(
        ForeignKey("document_collections.id"),
        nullable=True,
    )

    is_favorite: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_archived: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    owner = relationship(
        "User",
        back_populates="chats",
    )

    collection = relationship(
        "Collection",
    )

    messages = relationship(
        "ChatMessage",
        back_populates="chat",
        cascade="all, delete-orphan",
    )