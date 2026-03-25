import enum
import uuid
from datetime import datetime
from sqlalchemy import String, ForeignKey, Text, Float, Integer, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from app.models.base import Base

class AttemptStatus(str, enum.Enum):
    waiting = "waiting"
    registered = "registered"
    started = "started"
    submitted = "submitted"
    timed_out = "timed_out"

class CandidateAttempt(Base):
    __tablename__ = "candidate_attempts"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("test_sessions.id"), nullable=True)
    candidate_token: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)
    candidate_name: Mapped[str] = mapped_column(String(255), nullable=False)
    candidate_email: Mapped[str] = mapped_column(String(255), nullable=False)
    assigned_problem_id: Mapped[str | None] = mapped_column(ForeignKey("problems.id"), nullable=True)
    time_limit_minutes: Mapped[int] = mapped_column(Integer, default=45)
    admin_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("admins.id"), nullable=True)
    status: Mapped[AttemptStatus] = mapped_column(SAEnum(AttemptStatus), default=AttemptStatus.registered)
    submitted_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    language: Mapped[str | None] = mapped_column(String(20), nullable=True)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    passed_cases: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_cases: Mapped[int | None] = mapped_column(Integer, nullable=True)
    test_results: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    time_taken_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    session = relationship("TestSession", back_populates="attempts")
    problem = relationship("Problem") # Keep for legacy/single compat
    problems = relationship("CandidateProblem", back_populates="attempt", cascade="all, delete-orphan")
    admin = relationship("Admin")
