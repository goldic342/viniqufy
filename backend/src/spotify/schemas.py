from pydantic import BaseModel, Field

from src.models import Playlist, Track, Artist


# TODO: find way to avoid code duplication
class SpotifyPlaylist(Playlist):
    spotify_id: str
    description: str
    followers: int


class SpotifyPlaylistCreate(BaseModel):
    spotify_id: str


class SpotifyArtist(Artist):
    spotify_id: str
    genres: list[str]
    popularity: int = Field(ge=0, le=100)


class SpotifyTrackAnalysis(BaseModel):
    spotify_id: str
    tempo: float
    key: int
    mode: int = Field(ge=0, le=1)
    loudness: float
    duration: float
    energy: float = Field(ge=0, le=1)
    valence: float = Field(ge=0, le=1)
    danceability: float = Field(ge=0, le=1)


class SpotifyTrack(Track):
    spotify_id: str
    popularity: int = Field(ge=0, le=100)
    artists: list[SpotifyArtist]  # override default property
    analysis: SpotifyTrackAnalysis
    release_year: int
