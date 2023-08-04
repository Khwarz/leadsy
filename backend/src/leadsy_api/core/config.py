from functools import lru_cache
from typing import Any

from pydantic import validator
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

    @property
    def database_uri(self) -> str:
        username = self.db_user
        password = self.db_password
        host = self.db_host
        port = self.db_port
        return f"postgresql://{username}:{password}@{host}:{port}/{self.db_database}"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
