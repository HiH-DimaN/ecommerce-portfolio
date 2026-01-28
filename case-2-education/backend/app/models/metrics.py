from datetime import date

from sqlalchemy import Date, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin, UUIDMixin


class DailyMetrics(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "daily_metrics"

    date: Mapped[date] = mapped_column(Date, unique=True, nullable=False)
    total_students: Mapped[int | None] = mapped_column(Integer)
    active_students: Mapped[int | None] = mapped_column(Integer)
    completed_courses: Mapped[int | None] = mapped_column(Integer)
    ai_questions_answered: Mapped[int | None] = mapped_column(Integer)
    ai_resolution_rate: Mapped[float | None] = mapped_column(Numeric(5, 2))
    retention_rate: Mapped[float | None] = mapped_column(Numeric(5, 2))
