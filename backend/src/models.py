from uuid import UUID, uuid4

from pydantic import BaseModel


class Playlist(BaseModel):
    name: str
    owner: str
    id: UUID = uuid4()
    tracks_count: int


class Artist(BaseModel):
    name: str
    id: UUID = uuid4()


class Track(BaseModel):
    name: str
    id: UUID = uuid4()
    artists: list[Artist]
