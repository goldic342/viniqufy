from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    weights: dict[str, float] = {
        'popularity': 0.3,
        'artist_diversity': 0.2,
        'musical_diversity': 0.1,
        'genre_diversity': 0.2,
        'temporal_diversity': 0.1,
        'era_diversity': 0.1
    }

    rate_limit_wait: int = 5


settings = Settings()
