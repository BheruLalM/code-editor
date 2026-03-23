from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 8
    FRONTEND_URL: str
    ALLOWED_ORIGINS: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
