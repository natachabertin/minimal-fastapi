from functools import cached_property

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Minimal FastAPI Sample"
    # Server config
    api_prefix: str = "/api"
    version: str

    # Server security
    allowed_origins: list = ["*"]
    allowed_methods: list = ["*"]
    allowed_headers: list = ["*"]

    # PG DB config
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db_name: str

    model_config = SettingsConfigDict(env_file="../../.env", extra='ignore')

    @computed_field
    @cached_property
    def db_url(self) -> int:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db_name}"


