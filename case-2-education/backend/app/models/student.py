import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class StudentStatus(str, Enum):
    ACTIVE = "active"
    AT_RISK = "at_risk"
    DROPPED = "dropped"
    COMPLETED = "completed"


class ProgressStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Student(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "students"

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255))
    avatar_url: Mapped[str | None] = mapped_column(String(500))
    enrolled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default="now()"
    )
    last_active_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[StudentStatus] = mapped_column(String(50), default=StudentStatus.ACTIVE)
    risk_score: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User | None"] = relationship("User", back_populates="student")
    progress: Mapped[list["StudentProgress"]] = relationship(
        "StudentProgress", back_populates="student", cascade="all, delete-orphan"
    )
    chat_sessions: Mapped[list["ChatSession"]] = relationship(
        "ChatSession", back_populates="student", cascade="all, delete-orphan"
    )
    homework_submissions: Mapped[list["HomeworkSubmission"]] = relationship(
        "HomeworkSubmission", back_populates="student", cascade="all, delete-orphan"
    )
    test_results: Mapped[list["TestResult"]] = relationship(
        "TestResult", back_populates="student", cascade="all, delete-orphan"
    )
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification", back_populates="student", cascade="all, delete-orphan"
    )


class StudentProgress(Base, UUIDMixin):
    __tablename__ = "student_progress"
    __table_args__ = (UniqueConstraint("student_id", "lesson_id", name="uq_student_lesson"),)

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id"), nullable=False, index=True
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False
    )
    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False
    )
    status: Mapped[ProgressStatus] = mapped_column(
        String(50), default=ProgressStatus.NOT_STARTED
    )
    progress_percent: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    student: Mapped["Student"] = relationship("Student", back_populates="progress")
    course: Mapped["Course"] = relationship("Course")
    lesson: Mapped["Lesson"] = relationship("Lesson")
