import logging as log
from functools import cached_property, lru_cache
from pathlib import Path
import sys

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Server config
    app_name: str = "Minimal FastAPI Sample"
    api_prefix: str = "/api"
    version: str

    # Environment config
    environment: str = "dev"
    db_echo: bool = False

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

    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parent / "../../.env", extra='ignore')

    @computed_field
    @cached_property
    def db_url(self) -> str:
        db_link = f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db_name}"
        if "pytest" in sys.modules:
            log.debug("-----> Working with TEST db")
            db_link += "_test"

        return db_link


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
