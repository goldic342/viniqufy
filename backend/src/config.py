from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SPOTIFY_CLIENT_ID: str
    SPOTIFY_CLIENT_SECRET: str

    model_config = SettingsConfigDict(env_file=".env")


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
