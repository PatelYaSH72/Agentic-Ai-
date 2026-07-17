from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # =========================
    # Application
    # =========================
    APP_NAME: str = "Enterprise RAG Studio"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # =========================
    # Database
    # =========================
    DATABASE_URL: str

    # =========================
    # JWT
    # =========================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # =========================
    # Uploads
    # =========================
    UPLOAD_DIR: str = "uploads"

    # =========================
    # Logging
    # =========================
    LOG_DIR: str = "logs"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()