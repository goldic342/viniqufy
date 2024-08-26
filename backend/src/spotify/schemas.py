from pydantic import BaseModel

from src.models import Playlist


class SpotifyPlaylist(Playlist):
    spotify_id: str
    description: str
    followers: int


class SpotifyPlaylistCreate(BaseModel):
    spotify_id: str