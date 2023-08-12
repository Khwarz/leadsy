from functools import lru_cache

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str
    api_version: str = "v1"
    app_key: str
    postgres_db: str
    postgres_host: str
    postgres_port: str
    postgres_user: str
    postgres_password: str
    access_token_expires_minutes: int = 54600

    mail_host: str
    mail_port: int
    mail_username: str
    mail_password: str
    mail_tls: bool
    mail_from_address: str
    mail_from_name: str

    @computed_field  # type: ignore[misc]
    @property
    def database_uri(self) -> str:
        username = self.postgres_user
        password = self.postgres_password
        host = self.postgres_host
        port = self.postgres_port
        return f"postgresql://{username}:{password}@{host}:{port}/{self.postgres_db}"

    @computed_field  # type: ignore[misc]
    @property
    def test_database_uri(self) -> str:
        username = self.postgres_user
        password = self.postgres_password
        host = self.postgres_host
        port = self.postgres_port
        return f"postgresql://{username}:{password}@{host}:{port}/testing"


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
