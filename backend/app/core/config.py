from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Minimal FastAPI Sample"
    # Server config
    api_prefix: str = "/api"
    version: str

    # PG DB config
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_db_name: str

    model_config = SettingsConfigDict(env_file="../../.env", extra='ignore')


