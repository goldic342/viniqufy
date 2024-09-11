from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from src.models import TaskInitialization, Task


# TODO: find way to avoid code duplication
class Playlist(BaseModel):
    name: str
    owner: str | None
    id: UUID = uuid4()
    tracks_count: int
    spotify_id: str
    image_url: str
    description: str


class SpotifyPlaylistStart(BaseModel):
    spotify_id: str


class Artist(BaseModel):
    name: str
    id: UUID = uuid4()
    spotify_id: str
    genres: list[str]
    popularity: int = Field(ge=0, le=100)


class TrackAnalysis(BaseModel):
    spotify_id: str
    tempo: float
    key: int
    mode: int = Field(ge=0, le=1)
    loudness: float
    duration: float
    energy: float = Field(ge=0, le=1)
    valence: float = Field(ge=0, le=1)
    danceability: float = Field(ge=0, le=1)


class SpotifyTrack(BaseModel):
    name: str
    id: UUID = uuid4()
    artists: list[Artist]
    spotify_id: str
    popularity: int = Field(ge=0, le=100)
    analysis: TrackAnalysis
    release_year: int


class SpotifyTask(Task):
    result: Optional[float] = None


class SpotifyTaskInitialization(TaskInitialization):
    info: Playlist
