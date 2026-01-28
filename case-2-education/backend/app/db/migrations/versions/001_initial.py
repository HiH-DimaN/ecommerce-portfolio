"""Initial migration - create all tables

Revision ID: 001_initial
Revises: 
Create Date: 2025-01-27

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False, unique=True, index=True),
        sa.Column("telegram_username", sa.String(255)),
        sa.Column("first_name", sa.String(255)),
        sa.Column("last_name", sa.String(255)),
        sa.Column("photo_url", sa.String(500)),
        sa.Column("role", sa.String(50), server_default="student"),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "courses",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("total_lessons", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "students",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255)),
        sa.Column("avatar_url", sa.String(500)),
        sa.Column("enrolled_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("last_active_at", sa.DateTime(timezone=True)),
        sa.Column("status", sa.String(50), server_default="active"),
        sa.Column("risk_score", sa.Integer(), server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_students_status", "students", ["status"])
    op.create_index("ix_students_risk_score", "students", ["risk_score"])

    op.create_table(
        "lessons",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("courses.id"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("content_type", sa.String(50)),
        sa.Column("duration_minutes", sa.Integer()),
        sa.Column("is_locked", sa.Boolean(), server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "student_progress",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id"), nullable=False, index=True),
        sa.Column("course_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("courses.id"), nullable=False),
        sa.Column("lesson_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("lessons.id"), nullable=False),
        sa.Column("status", sa.String(50), server_default="not_started"),
        sa.Column("progress_percent", sa.Integer(), server_default="0"),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.UniqueConstraint("student_id", "lesson_id", name="uq_student_lesson"),
    )

    op.create_table(
        "tests",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("lesson_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("lessons.id"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("max_score", sa.Integer(), server_default="100"),
        sa.Column("passing_score", sa.Integer(), server_default="70"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "test_results",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id"), nullable=False),
        sa.Column("test_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("tests.id"), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "homework",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("lesson_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("lessons.id"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("due_days", sa.Integer(), server_default="7"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "homework_submissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id"), nullable=False),
        sa.Column("homework_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("homework.id"), nullable=False),
        sa.Column("content", sa.Text()),
        sa.Column("file_url", sa.String(500)),
        sa.Column("status", sa.String(50), server_default="pending"),
        sa.Column("ai_score", sa.Integer()),
        sa.Column("ai_feedback", sa.Text()),
        sa.Column("curator_score", sa.Integer()),
        sa.Column("curator_feedback", sa.Text()),
        sa.Column("submitted_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("reviewed_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "chat_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id"), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("ended_at", sa.DateTime(timezone=True)),
    )

    op.create_table(
        "chat_messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("chat_sessions.id"), nullable=False, index=True),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("response_time_ms", sa.Integer()),
        sa.Column("resolved_by_ai", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "knowledge_embeddings",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("embedding", postgresql.ARRAY(sa.Float()), nullable=True),
        sa.Column("source_type", sa.String(50)),
        sa.Column("source_id", postgresql.UUID(as_uuid=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("message", sa.Text()),
        sa.Column("student_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("students.id")),
        sa.Column("read", sa.Boolean(), server_default="false", index=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "daily_metrics",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("date", sa.Date(), nullable=False, unique=True),
        sa.Column("total_students", sa.Integer()),
        sa.Column("active_students", sa.Integer()),
        sa.Column("completed_courses", sa.Integer()),
        sa.Column("ai_questions_answered", sa.Integer()),
        sa.Column("ai_resolution_rate", sa.Numeric(5, 2)),
        sa.Column("retention_rate", sa.Numeric(5, 2)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("daily_metrics")
    op.drop_table("notifications")
    op.drop_table("knowledge_embeddings")
    op.drop_table("chat_messages")
    op.drop_table("chat_sessions")
    op.drop_table("homework_submissions")
    op.drop_table("homework")
    op.drop_table("test_results")
    op.drop_table("tests")
    op.drop_table("student_progress")
    op.drop_table("lessons")
    op.drop_table("students")
    op.drop_table("courses")
    op.drop_table("users")
    op.execute("DROP EXTENSION IF EXISTS vector")
