from datetime import date, datetime, timedelta
from uuid import UUID, uuid4

from sqlalchemy import text, ForeignKey, Table, Column, String, Enum as SQLAlchemyEnum, UUID as SQLALCHEMY_UUID, \
    DateTime
from sqlalchemy.orm import mapped_column, Mapped, validates, relationship, declared_attr

from src.analysis.enums import AnalysisStatus
from src.analysis.enums import Genre as GenreEnum
from src.analysis.utils import validate_popularity
from src.config import settings
from src.database import Base


class BaseTable(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


class ExpireTable(BaseTable):
    __abstract__ = True
    updated_at: Mapped[datetime] = mapped_column(onupdate=text("TIMEZONE('utc', now())"))

    @declared_attr
    def expires_at(self) -> Mapped[datetime]:
        return mapped_column(DateTime, default=lambda: datetime.now() + timedelta(days=self.expiers_after))


# Association tables
artist_genre_association = Table(
    'artist_genre_association',
    Base.metadata,
    Column('artist_id', String, ForeignKey("artist.artist_id")),
    Column('genre_id', String, ForeignKey("genre.name")),
)

artist_track_association = Table(
    'artist_track_association',
    Base.metadata,
    Column('artist_id', String, ForeignKey("artist.artist_id")),
    Column('track_id', String, ForeignKey("track.track_id")),
)

playlist_track_association = Table(
    'playlist_track_association',
    Base.metadata,
    Column('playlist_version_id', SQLALCHEMY_UUID, ForeignKey("playlist_version.version_id")),
    Column('track_id', String, ForeignKey("track.track_id")),
)


class Playlist(BaseTable):
    __tablename__ = "playlist"

    playlist_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, unique=True)
    spotify_playlist_id: Mapped[str] = mapped_column(unique=True)
    current_snapshot_id: Mapped[str]

    versions: Mapped[list["PlaylistVersion"]] = relationship("PlaylistVersion", back_populates="playlist",
                                                             order_by="PlaylistVersion.created_at.desc()")


class PlaylistVersion(BaseTable):
    __tablename__ = "playlist_version"

    version_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, unique=True)
    playlist_id: Mapped[UUID] = mapped_column(ForeignKey("playlist.playlist_id"))
    snapshot_id: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    description: Mapped[str]
    owner_name: Mapped[str]
    owner_spotify_id: Mapped[str]
    followers: Mapped[int]
    tracks_count: Mapped[int]

    playlist: Mapped["Playlist"] = relationship("Playlist", back_populates="versions")
    analysis: Mapped["Analysis"] = relationship("Analysis", back_populates="playlist_version", uselist=False)
    tracks: Mapped[list["Track"]] = relationship("Track", secondary=playlist_track_association,
                                                 back_populates="playlist_versions")


class Analysis(BaseTable):
    __tablename__ = "analysis"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, unique=True)
    playlist_version_id: Mapped[UUID] = mapped_column(ForeignKey("playlist_version.version_id"))
    status: Mapped[AnalysisStatus] = mapped_column(SQLAlchemyEnum(AnalysisStatus), default=AnalysisStatus.PENDING)
    task_id: Mapped[str] = mapped_column(nullable=True)

    # Analysis data (nullable for pending analysis)
    uniqueness: Mapped[float] = mapped_column(nullable=True)
    # Other metrics will be added later

    playlist_version: Mapped["PlaylistVersion"] = relationship("PlaylistVersion", back_populates="analysis")


class Track(ExpireTable):
    __tablename__ = "track"

    track_id: Mapped[str] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str]
    release_date: Mapped[date]
    explicit: Mapped[bool]
    popularity: Mapped[int]

    expires_after = settings.TRACK_EXPIRY_DAYS

    track_features: Mapped["TrackFeatures"] = relationship("TrackFeatures", back_populates="track", uselist=False)
    artists: Mapped[list["Artist"]] = relationship("Artist", secondary=artist_track_association,
                                                   back_populates='tracks')
    playlist_versions: Mapped[list["PlaylistVersion"]] = relationship("PlaylistVersion",
                                                                      secondary=playlist_track_association,
                                                                      back_populates="tracks")

    @validates('popularity')
    def validate_popularity(self, key, value):
        return validate_popularity(value)


class TrackFeatures(BaseTable):
    __tablename__ = "track_features"

    track_id: Mapped[str] = mapped_column(ForeignKey("track.track_id"), primary_key=True, unique=True)

    # Nullable = True because some all metrics not implemented yet
    dance_ability: Mapped[float] = mapped_column(nullable=True)
    energy: Mapped[float] = mapped_column(nullable=True)
    key: Mapped[int] = mapped_column(nullable=True)
    loudness: Mapped[float] = mapped_column(nullable=True)
    mode: Mapped[int] = mapped_column(nullable=True)
    speechiness: Mapped[float] = mapped_column(nullable=True)
    acousticness: Mapped[float] = mapped_column(nullable=True)
    instrumentalness: Mapped[float] = mapped_column(nullable=True)
    liveness: Mapped[float] = mapped_column(nullable=True)
    valence: Mapped[float] = mapped_column(nullable=True)
    tempo: Mapped[float] = mapped_column(nullable=True)
    duration_ms: Mapped[int] = mapped_column(nullable=True)
    time_signature: Mapped[int] = mapped_column(nullable=True)

    track: Mapped["Track"] = relationship("Track", back_populates="track_features")


class Artist(ExpireTable):
    __tablename__ = "artist"

    artist_id: Mapped[str] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str]
    followers: Mapped[int]
    popularity: Mapped[int]

    expires_after = settings.ARTIST_EXPIRY_DAYS

    genres: Mapped[list["Genre"]] = relationship('Genre', secondary=artist_genre_association, back_populates="artists")
    tracks: Mapped[list["Track"]] = relationship("Track", secondary=artist_track_association, back_populates="artists")

    @validates('popularity')
    def validate_popularity(self, key, value):
        return validate_popularity(value)


class Genre(Base):
    __tablename__ = 'genre'

    name: Mapped[str] = mapped_column(primary_key=True, unique=True)
    artists: Mapped[list["Artist"]] = relationship("Artist", secondary=artist_genre_association,
                                                   back_populates="genres")

    @validates('name')
    def validate_value(self, key, name):
        if not (name in [genre.value for genre in GenreEnum] or isinstance(name, str)):
            raise ValueError(f"Value must be one of {GenreEnum} or any string")
        return name
