import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class ContentType(str, Enum):
    VIDEO = "video"
    TEXT = "text"
    QUIZ = "quiz"


class Course(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "courses"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    total_lessons: Mapped[int] = mapped_column(Integer, nullable=False)

    lessons: Mapped[list["Lesson"]] = relationship(
        "Lesson", back_populates="course", cascade="all, delete-orphan", order_by="Lesson.order_index"
    )


class Lesson(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "lessons"

    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[ContentType | None] = mapped_column(String(50))
    duration_minutes: Mapped[int | None] = mapped_column(Integer)
    is_locked: Mapped[bool] = mapped_column(Boolean, default=False)

    course: Mapped["Course"] = relationship("Course", back_populates="lessons")
    tests: Mapped[list["Test"]] = relationship(
        "Test", back_populates="lesson", cascade="all, delete-orphan"
    )
    homework: Mapped[list["Homework"]] = relationship(
        "Homework", back_populates="lesson", cascade="all, delete-orphan"
    )


class Test(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "tests"

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("lessons.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    max_score: Mapped[int] = mapped_column(Integer, default=100)
    passing_score: Mapped[int] = mapped_column(Integer, default=70)

    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="tests")
    results: Mapped[list["TestResult"]] = relationship(
        "TestResult", back_populates="test", cascade="all, delete-orphan"
    )


class TestResult(Base, UUIDMixin):
    __tablename__ = "test_results"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id"), nullable=False
    )
    test_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tests.id"), nullable=False
    )
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default="now()"
    )

    student: Mapped["Student"] = relationship("Student", back_populates="test_results")
    test: Mapped["Test"] = relationship("Test", back_populates="results")
