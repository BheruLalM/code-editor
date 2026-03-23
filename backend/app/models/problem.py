import enum
from sqlalchemy import String, Text, Integer, Enum as SAEnum, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.sql import func
from datetime import datetime
from app.models.base import Base

class DifficultyLevel(str, enum.Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"

class Problem(Base):
    __tablename__ = "problems"

    id: Mapped[str] = mapped_column(String(10), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    difficulty: Mapped[DifficultyLevel] = mapped_column(SAEnum(DifficultyLevel), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    constraints: Mapped[str | None] = mapped_column(Text, nullable=True)
    examples: Mapped[list] = mapped_column(JSONB, nullable=False)
    starter_code: Mapped[dict] = mapped_column(JSONB, nullable=False)
    visible_test_cases: Mapped[list] = mapped_column(JSONB, nullable=False)
    hidden_test_cases: Mapped[list] = mapped_column(JSONB, nullable=False)
    time_limit_seconds: Mapped[int] = mapped_column(Integer, default=5)
    tags: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
