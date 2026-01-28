import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class SubmissionStatus(str, Enum):
    PENDING = "pending"
    AI_CHECKED = "ai_checked"
    CURATOR_REVIEWED = "curator_reviewed"


class Homework(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "homework"

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    due_days: Mapped[int] = mapped_column(Integer, default=7)

    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="homework")
    submissions: Mapped[list["HomeworkSubmission"]] = relationship(
        "HomeworkSubmission", back_populates="homework", cascade="all, delete-orphan"
    )


class HomeworkSubmission(Base, UUIDMixin):
    __tablename__ = "homework_submissions"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id"), nullable=False
    )
    homework_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("homework.id"), nullable=False
    )
    content: Mapped[str | None] = mapped_column(Text)
    file_url: Mapped[str | None] = mapped_column(String(500))
    status: Mapped[SubmissionStatus] = mapped_column(
        String(50), default=SubmissionStatus.PENDING
    )
    ai_score: Mapped[int | None] = mapped_column(Integer)
    ai_feedback: Mapped[str | None] = mapped_column(Text)
    curator_score: Mapped[int | None] = mapped_column(Integer)
    curator_feedback: Mapped[str | None] = mapped_column(Text)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default="now()"
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    student: Mapped["Student"] = relationship("Student", back_populates="homework_submissions")
    homework: Mapped["Homework"] = relationship("Homework", back_populates="submissions")
