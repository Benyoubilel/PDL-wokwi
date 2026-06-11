from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "SmartWeatherAI"
    DEBUG: bool = True

    API_PREFIX: str = "/api/v1"

    API_BASE: str = "http://localhost:8000/api/v1"
    REFRESH_INTERVAL: int = 10

    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[3] / ".env",
        extra="ignore"
    )


settings = Settings()