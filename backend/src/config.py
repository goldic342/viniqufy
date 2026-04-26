from os import path
from pathlib import Path
from typing import Any

from pydantic import PostgresDsn, field_validator
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    IS_PROD: bool = True

    DATA_DIR: Path = Path("./data")
    LOG_DIR: Path = DATA_DIR / "logs"

    ORIGINS: str = "http://localhost:5173"

    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str

    DATABASE_USER: str
    DATABASE_HOST: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_URI: PostgresDsn | str = ""

    @field_validator("DATABASE_URI", mode="after")
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

    model_config = SettingsConfigDict(
        env_file=path.join(path.dirname(path.abspath(__file__)), "..", ".env"),
        extra="ignore",
    )


class CeleryConfig:
    broker_url = "redis://localhost:6379"
    result_backend = "redis://localhost:6379/0"

    # Pydantic schemas support
    task_serializer = "pickle"
    result_serializer = "pickle"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json", "application/x-python-serialize"]

    imports = ("analysis.tasks",)

    task_annotations = {"analysis.tasks": {"rate_limit": "100/m"}}

    # Celery 6.0+ specific configuration
    broker_connection_retry_on_startup = True

    # Add CREATED property to task status
    task_track_started = True


settings = Settings()  # type: ignore
