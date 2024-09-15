from typing import Any

from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DEBUG_MODE: bool = False

    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str

    DATABASE_USER: str
    DATABASE_HOST: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    ASYNC_DATABASE_URI: PostgresDsn | str = ""

    @field_validator("ASYNC_DATABASE_URI", mode="after")
    def assemble_db_connection(cls, v: str | None, info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            if v == "":
                return PostgresDsn.build(
                    scheme="postgresql+asyncpg",
                    username=info.data["DATABASE_USER"],
                    password=info.data["DATABASE_PASSWORD"],
                    host=info.data["DATABASE_HOST"],
                    port=info.data["DATABASE_PORT"],
                    path=info.data["DATABASE_NAME"],
                )
        return v

    TRACK_EXPIRY_DAYS: int = 7
    ARTIST_EXPIRY_DAYS: int = 7

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


class CeleryConfig:
    broker_url = 'redis://localhost:6379'
    result_backend = 'redis://localhost:6379/0'

    # Pydantic schemas support
    task_serializer = "pickle"
    result_serializer = "pickle"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json", "application/x-python-serialize"]

    imports = ('src.analysis.tasks',)

    task_annotations = {
        'src.analysis.tasks': {'rate_limit': '100/m'}
    }

    task_track_started = True


settings = Settings()
