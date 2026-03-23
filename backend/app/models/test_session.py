import enum
import uuid
from datetime import datetime
from sqlalchemy import String, Text, Integer, Boolean, ForeignKey, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import Base, TimestampMixin

class DifficultyFilter(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"
    any = "any"

class TestSession(Base, TimestampMixin):
    __tablename__ = "test_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_token: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    difficulty_filter: Mapped[DifficultyFilter] = mapped_column(SAEnum(DifficultyFilter), default=DifficultyFilter.any)
    time_limit_minutes: Mapped[int] = mapped_column(Integer, default=45)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    max_attempts: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("admins.id"), nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    admin = relationship("Admin")
    attempts = relationship("CandidateAttempt", back_populates="session")
