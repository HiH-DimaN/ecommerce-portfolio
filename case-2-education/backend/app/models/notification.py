import uuid
from enum import Enum

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class NotificationType(str, Enum):
    HOMEWORK_SUBMITTED = "homework_submitted"
    LESSON_COMPLETED = "lesson_completed"
    STUDENT_AT_RISK = "student_at_risk"
    TEST_PASSED = "test_passed"
    COURSE_COMPLETED = "course_completed"


class Notification(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "notifications"

    type: Mapped[NotificationType] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str | None] = mapped_column(Text)
    student_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id")
    )
    read: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    student: Mapped["Student | None"] = relationship("Student", back_populates="notifications")
