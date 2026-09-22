from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    max_text_length: int = 10_000
    max_image_size_mb: int = 5
    model_path: str = str(Path(__file__).resolve().parents[2] / "models" / "text_classifier.joblib")
    cors_origins: str = "http://localhost:5173"
    rate_limit: str = "60/minute"

    @property
    def cors_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
