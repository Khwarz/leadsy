from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str
    app_key: str
    postgres_db: str
    postgres_host: str
    postgres_port: str
    postgres_user: str
    postgres_password: str

    @property
    def database_uri(self) -> str:
        username = self.postgres_user
        password = self.postgres_password
        host = self.postgres_host
        port = self.postgres_port
        return f"postgresql://{username}:{password}@{host}:{port}/{self.postgres_db}"

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
