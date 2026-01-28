import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class SourceType(str, Enum):
    LESSON = "lesson"
    FAQ = "faq"
    GRAMMAR_RULE = "grammar_rule"


class ChatSession(Base, UUIDMixin):
    __tablename__ = "chat_sessions"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id"), nullable=False
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default="now()"
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    student: Mapped["Student"] = relationship("Student", back_populates="chat_sessions")
    messages: Mapped[list["ChatMessage"]] = relationship(
        "ChatMessage", back_populates="session", cascade="all, delete-orphan", order_by="ChatMessage.created_at"
    )


class ChatMessage(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "chat_messages"

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("chat_sessions.id"), nullable=False, index=True
    )
    role: Mapped[MessageRole] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    response_time_ms: Mapped[int | None] = mapped_column(Integer)
    resolved_by_ai: Mapped[bool] = mapped_column(Boolean, default=True)

    session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="messages")


class KnowledgeEmbedding(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "knowledge_embeddings"

    content: Mapped[str] = mapped_column(Text, nullable=False)
    source_type: Mapped[SourceType | None] = mapped_column(String(50))
    source_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
