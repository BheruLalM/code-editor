import enum
import uuid
from sqlalchemy import String, ForeignKey, Text, Float, Integer, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.models.base import Base

class ProblemStatus(str, enum.Enum):
    assigned = "assigned"
    started = "started"
    submitted = "submitted"

class CandidateProblem(Base):
    __tablename__ = "candidate_problems"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attempt_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("candidate_attempts.id", ondelete="CASCADE"), nullable=False)
    problem_id: Mapped[str] = mapped_column(ForeignKey("problems.id"), nullable=False)
    
    status: Mapped[ProblemStatus] = mapped_column(SAEnum(ProblemStatus), default=ProblemStatus.assigned)
    submitted_code: Mapped[str | None] = mapped_column(Text, nullable=True)
    language: Mapped[str | None] = mapped_column(String(20), nullable=True)
    score: Mapped[float | None] = mapped_column(Float, nullable=True)
    passed_cases: Mapped[int | None] = mapped_column(Integer, nullable=True)
    total_cases: Mapped[int | None] = mapped_column(Integer, nullable=True)
    test_results: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    attempt = relationship("CandidateAttempt", back_populates="problems")
    problem = relationship("Problem")
