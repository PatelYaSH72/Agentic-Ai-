from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.database import Base


class RetrievalLog(Base):
    __tablename__ = "retrieval_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    message_id: Mapped[int] = mapped_column(
        ForeignKey("chat_messages.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    retrieval_strategy: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    query: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    expanded_query: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    hyde_query: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    top_k: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    retrieved_chunks: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    average_similarity_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    retrieval_time_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    reranking_enabled: Mapped[bool] = mapped_column(
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    message = relationship(
        "ChatMessage",
        back_populates="retrieval_log",
    )