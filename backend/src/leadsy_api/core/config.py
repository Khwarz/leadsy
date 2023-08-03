from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str
    app_key: str
    db_database: str
    db_host: str
    db_port: str
    db_user: str
    db_password: str


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
