from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from src.analysis.enums import AnalysisStatus, Genre
from src.models import TaskResult, TaskInit


class SPlaylistCreate(BaseModel):
    spotify_playlist_id: str


class SPlaylistBase(SPlaylistCreate):
    playlist_id: Optional[UUID] = None
    current_snapshot_id: str


class SPlaylistVersionBase(BaseModel):
    version_id: Optional[UUID] = None
    playlist_id: UUID
    snapshot_id: str
    name: str
    description: str
    owner_name: str
    owner_spotify_id: str
    followers: int
    tracks_count: int


class SAnalysisBase(BaseModel):
    id: Optional[UUID] = None
    playlist_version_id: UUID
    status: AnalysisStatus
    task_id: UUID = None
    uniqueness: Optional[float] = None


class SAnalysisUpdate(BaseModel):
    status: Optional[AnalysisStatus] = None
    uniqueness: Optional[float] = None


class STrackBase(BaseModel):
    track_id: str
    name: str
    release_date: date
    explicit: bool
    popularity: int = Field(ge=0, le=100)


class STrackFeaturesBase(BaseModel):
    track_id: str
    dance_ability: Optional[float] = None
    energy: Optional[float] = None
    key: Optional[int] = None
    loudness: Optional[float] = None
    mode: Optional[int] = None
    speechiness: Optional[float] = None
    acousticness: Optional[float] = None
    instrumentalness: Optional[float] = None
    liveness: Optional[float] = None
    valence: Optional[float] = None
    tempo: Optional[float] = None
    duration_ms: Optional[int] = None
    time_signature: Optional[int] = None


class SArtistBase(BaseModel):
    artist_id: str
    name: str
    followers: int
    popularity: int = Field(ge=0, le=100)
    genres: list[Genre]


class SArtist(SArtistBase):
    tracks: list['STrackBase'] = []


class STrackFeatures(STrackFeaturesBase):
    track: 'STrackBase'


class STrack(STrackBase):
    track_features: Optional[STrackFeaturesBase] = None
    artists: list[SArtistBase] = []
    playlist_versions: list['SPlaylistVersionBase'] = []


class SAnalysis(SAnalysisBase):
    playlist_version: 'SPlaylistVersionBase'


class SPlaylistVersion(SPlaylistVersionBase):
    playlist: 'SPlaylistBase'
    analysis: Optional[SAnalysisBase] = None
    tracks: list[STrackBase] = []


class SPlaylist(SPlaylistBase):
    versions: list[SPlaylistVersionBase] = []


class SPlaylistInfo(BaseModel):
    """
    SPlaylistInfo used in fronted as playlist info. Not recommended to use as a model for operations
    """
    image_url: str
    spotify_playlist_id: str
    snapshot_id: str
    name: str
    description: str
    owner_name: str
    owner_spotify_id: str
    followers: int
    tracks_count: int

    @classmethod
    def from_base_and_version(cls, base: SPlaylistBase | SPlaylist, version: SPlaylistVersionBase,
                              image_url: str) -> 'SPlaylistInfo':
        combined_dict = {**base.dict(), **version.dict(), "image_url": image_url}

        # Creating new instance
        return cls(**combined_dict)


# Update forward refs
STrack.update_forward_refs()
SPlaylistVersion.update_forward_refs()
SPlaylist.update_forward_refs()


# Analysis Task schemas
class AnalysisTaskResult(TaskResult):
    result: Optional[float]


class AnalysisTaskInit(TaskInit):
    info: 'SPlaylistInfo'
