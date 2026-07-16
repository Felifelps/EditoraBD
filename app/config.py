from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://root:root@localhost:5432/root"
    secret_key: str = "dev-secret-troque-em-producao"
    session_cookie_name: str = "session"
    session_max_age: int = 60 * 60 * 8  # 8 horas


@lru_cache
def get_settings() -> Settings:
    return Settings()
