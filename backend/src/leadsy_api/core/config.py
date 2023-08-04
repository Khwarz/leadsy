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
    database_uri: str | None = None

    @validator("database_uri", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        username = values.get("db_user")
        password = values.get("db_password")
        host = values.get("db_host")
        port = values.get("db_port")
        return f"postgresql://{username}:{password}@{host}:{port}/{values.get('db_database')}"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
