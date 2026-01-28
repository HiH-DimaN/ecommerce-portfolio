from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/education"
    REDIS_URL: str = "redis://localhost:6379"

    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 10080

    TELEGRAM_BOT_TOKEN: str = ""
    OPENAI_API_KEY: str = ""

    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "education"

    DEBUG: bool = True
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]


settings = Settings()
