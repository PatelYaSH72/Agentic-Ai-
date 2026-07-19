from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
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


class UserSettings(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    embedding_model: Mapped[str] = mapped_column(
        String(100),
        default="text-embedding-3-small",
    )

    retrieval_strategy: Mapped[str] = mapped_column(
        String(50),
        default="hybrid",
    )

    top_k: Mapped[int] = mapped_column(
        Integer,
        default=5,
    )

    similarity_threshold: Mapped[float] = mapped_column(
        Float,
        default=0.7,
    )

    temperature: Mapped[float] = mapped_column(
        Float,
        default=0.2,
    )

    streaming_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
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

    user = relationship(
        "User",
        back_populates="settings",
    )