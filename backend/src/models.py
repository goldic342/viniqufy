from uuid import UUID

from pydantic import BaseModel


class Playlist(BaseModel):
    name: str
    owner: str
    id: UUID
    tracks_count: int
