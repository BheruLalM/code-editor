from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 8
    FRONTEND_URL: str
    ALLOWED_ORIGINS: str = "http://localhost:5173"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        """
        Railway often provides PostgreSQL URLs as:
          - postgres://...
          - postgresql://...
        For async SQLAlchemy we must use asyncpg:
          - postgresql+asyncpg://...
        """
        if not isinstance(value, str):
            return value

        if value.startswith("postgresql+asyncpg://"):
            return value
        if value.startswith("postgres://"):
            return value.replace("postgres://", "postgresql+asyncpg://", 1)
        if value.startswith("postgresql://"):
            return value.replace("postgresql://", "postgresql+asyncpg://", 1)
        return value

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
