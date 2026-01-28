from enum import Enum

from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class UserRole(str, Enum):
    STUDENT = "student"
    CURATOR = "curator"
    ADMIN = "admin"


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False, index=True)
    telegram_username: Mapped[str | None] = mapped_column(String(255))
    first_name: Mapped[str | None] = mapped_column(String(255))
    last_name: Mapped[str | None] = mapped_column(String(255))
    photo_url: Mapped[str | None] = mapped_column(String(500))
    role: Mapped[UserRole] = mapped_column(String(50), default=UserRole.STUDENT)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    student: Mapped["Student | None"] = relationship(
        "Student", back_populates="user", uselist=False
    )
