from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.analysis.models import Track, TrackFeatures, Artist, Playlist, PlaylistVersion, Analysis
from src.analysis.schemas import STrack, STrackBase, SArtist, SArtistBase, SPlaylist, SPlaylistBase, \
    SPlaylistVersion, SPlaylistVersionBase, STrackFeaturesBase, SAnalysis, SAnalysisBase, SAnalysisUpdate
from src.repository import BaseRepository, with_session_management


# TODO: find way to avoid code duplication (lazy rn)

# NOTE:
# IDK how it will work with planned in the future dashboard.
# Most likely repo will be rewritten during admin dashboard development

@with_session_management
class TrackFeaturesRepository(BaseRepository):
    async def get(self, track_id: str) -> STrackFeaturesBase | None:
        query = (
            select(TrackFeatures)
            .options(joinedload(TrackFeatures.track))
            .where(TrackFeatures.track_id == track_id)
        )

        features_model = await self.session.execute(query)
        features_scalar = features_model.scalar_one_or_none()

        if not features_scalar:
            return None

        return STrackFeaturesBase.model_validate(features_scalar, from_attributes=True)

    async def create(self, input_features: STrackFeaturesBase) -> STrackFeaturesBase:
        features_model = TrackFeatures(**input_features.model_dump())

        self.session.add(features_model)
        await self.session.flush()
        await self.session.commit()

        return STrackFeaturesBase.model_validate(features_model, from_attributes=True)


@with_session_management
class ArtistsRepository(BaseRepository):

    async def get(self, artist_id: str) -> SArtist | None:
        query = (
            select(Artist)
            .options(selectinload(Artist.tracks))
            .where(Artist.artist_id == artist_id)
        )

        artist_model = await self.session.execute(query)
        artist_scalar = artist_model.scalar_one_or_none()

        if not artist_scalar:
            return None

        return SArtist.model_validate(artist_scalar, from_attributes=True)

    async def create(self, input_artist: SArtistBase) -> SArtistBase:
        artist_model = Artist(**input_artist.model_dump())

        self.session.add(artist_model)
        await self.session.flush()
        await self.session.commit()

        return SArtistBase.model_validate(artist_model, from_attributes=True)

    async def update(self, input_artist: SArtistBase) -> SArtistBase | None:
        """
        Updating artist attributes without relationships
        :param input_artist: schema of artist to update
        :return: updated artist schema (without relationships) or None if not found
        """
        artist_model = await self.session.get(Artist, input_artist.artist_id)

        if not artist_model:
            return None

        for key, value in input_artist.model_dump().items():
            setattr(artist_model, key, value)

        await self.session.flush()
        await self.session.commit()
        return SArtistBase.model_validate(artist_model, from_attributes=True)

    async def is_expired(self, artist_id: str) -> bool | None:
        """
        Compares artist expires_at date with current date
        :param artist_id: Spotify id of artist
        :return: True if expired, False if not or None if not found
        """
        artist_model = await self.session.get(Artist, artist_id)

        if not artist_model:
            return None

        return artist_model.expires_at < datetime.utcnow()

    async def add_track(self, artist_id: str, track_input: STrack) -> STrack | None:
        """
        Add track to artist
        :param artist_id: Spotify id of artist
        :param track_input: schema of track
        :return: added track schema or None if not found
        """
        artist_model = await self.session.get(Artist, artist_id)

        if not artist_model:
            return None

        track_model = Track(**track_input.model_dump())

        artist_model.tracks.append(track_model)
        await self.session.flush()
        await self.session.commit()
        return STrack.model_validate(track_model, from_attributes=True)


@with_session_management
class TrackRepository(BaseRepository):

    async def get(self, track_id: str) -> STrack | None:
        query = (
            select(Track)
            .options(
                joinedload(Track.track_features),
                selectinload(Track.playlist_versions),
                selectinload(Track.artists))
            .where(Track.track_id == track_id)
        )

        track_model = await self.session.execute(query)
        track_scalar = track_model.scalar_one_or_none()

        if not track_scalar:
            return None

        return STrack.model_validate(track_scalar, from_attributes=True)

    async def create(self, input_track: STrackBase) -> STrackBase:
        track_model = Track(**input_track.model_dump())

        self.session.add(track_model)
        await self.session.flush()
        await self.session.commit()

        return STrackBase.model_validate(track_model, from_attributes=True)

    async def update(self, input_track: STrackBase) -> STrack:
        """
        Updating track attributes without relationships
        :param input_track: schema of track to update
        :return: updated track schema (without relationships)
        """
        track_model = await self.get(input_track.track_id)

        for key, value in input_track.model_dump().items():
            setattr(track_model, key, value)

        await self.session.flush()
        await self.session.commit()
        return STrack.model_validate(track_model, from_attributes=True)

    async def set_features(self, track_id: str, features: STrackFeaturesBase) -> STrackBase | None:
        track_model = await self.session.get(Track, track_id)

        if not track_model:
            return None

        track_model.track_features = TrackFeatures(**features.model_dump())
        await self.session.flush()
        await self.session.commit()
        return STrackBase.model_validate(track_model, from_attributes=True)

    async def link_artist(self, input_artist: SArtistBase, track_id: str) -> None | STrackBase:
        """
        Linking existing artist to track
        :param input_artist: Schema of artist
        :param track_id: Spotify id of track
        :return: None if not found or added track schema
        """
        track_query = (
            select(Track)
            .where(Track.track_id == track_id)
            .options(selectinload(Track.artists))
        )
        track_model = await self.session.execute(track_query)
        track_model = track_model.scalar_one_or_none()
        artist_model = await self.session.get(Artist, input_artist.artist_id)

        if not track_model or not artist_model:
            return None

        track_model.artists.append(artist_model)
        await self.session.flush()
        await self.session.commit()

        return STrackBase.model_validate(track_model, from_attributes=True)

    async def is_expired(self, track_id: str) -> bool | None:
        """
        Compares track expires_at date with current date
        :param track_id: Spotify id of track
        :return: True if expired, False if not or None if not found
        """
        track_model = await self.session.get(Track, track_id)

        if not track_model:
            return None

        return track_model.expires_at < datetime.utcnow()


@with_session_management
class PlaylistRepository(BaseRepository):

    async def get(self, playlist_id: str) -> SPlaylist | None:
        query = (
            select(Playlist)
            .options(selectinload(Playlist.versions))
            .where(Playlist.spotify_playlist_id == playlist_id)
        )

        playlist_model = await self.session.execute(query)
        playlist_scalar = playlist_model.scalar_one_or_none()

        if not playlist_scalar:
            return None

        return SPlaylist.model_validate(playlist_scalar, from_attributes=True)

    async def create(self, input_playlist: SPlaylist) -> SPlaylist:
        playlist_model = Playlist(**input_playlist.model_dump())

        self.session.add(playlist_model)
        await self.session.flush()
        await self.session.commit()

        return SPlaylist.model_validate(playlist_model, from_attributes=True)

    async def update(self, input_playlist: SPlaylistBase) -> SPlaylistBase | None:
        """
        Updating playlist attributes without relationships
        :param input_playlist:
        :return:
        """
        playlist_model = await self.session.get(Playlist, input_playlist.playlist_id)

        if not playlist_model:
            return None

        for key, value in input_playlist.model_dump().items():
            setattr(playlist_model, key, value)

        await self.session.flush()
        await self.session.commit()
        return SPlaylistBase.model_validate(playlist_model, from_attributes=True)

    async def add_version(self, playlist_id: str, version_input: SPlaylistVersion) -> SPlaylistVersion | None:
        playlist_model = await self.session.get(Playlist, playlist_id)

        if not playlist_model:
            return None

        version_model = PlaylistVersion(**version_input.model_dump())

        playlist_model.versions.append(version_model)
        await self.session.flush()
        await self.session.commit()
        return SPlaylistVersion.model_validate(version_model, from_attributes=True)


@with_session_management
class PlaylistVersionRepository(BaseRepository):

    async def get(self, snapshot_id: str) -> SPlaylistVersion | None:
        query = (
            select(PlaylistVersion)
            .options(
                joinedload(PlaylistVersion.playlist),
                selectinload(PlaylistVersion.tracks),
                joinedload(PlaylistVersion.analysis)
            )
            .where(PlaylistVersion.snapshot_id == snapshot_id)
        )

        playlist_version_model = await self.session.execute(query)
        playlist_version_scalar = playlist_version_model.scalar_one_or_none()

        if not playlist_version_scalar:
            return None

        return SPlaylistVersion.model_validate(playlist_version_scalar, from_attributes=True)

    async def create(self, input_playlist_version: SPlaylistVersionBase) -> SPlaylistVersionBase:
        playlist_version_model = PlaylistVersion(**input_playlist_version.model_dump())

        self.session.add(playlist_version_model)
        await self.session.flush()
        await self.session.commit()

        return SPlaylistVersionBase.model_validate(playlist_version_model, from_attributes=True)

    async def link_track(self, input_track: STrack | STrackBase, version_id: UUID) -> None | SPlaylistVersionBase:
        """
        Linking existing artist to track
        :param input_track: Schema of track
        :param version_id: UUID of playlist version
        :return: None if not found or added track schema
        """
        playlist_version_query = (
            select(PlaylistVersion)
            .where(PlaylistVersion.version_id == version_id)
            .options(selectinload(PlaylistVersion.tracks))
        )

        playlist_version_model = await self.session.execute(playlist_version_query)
        playlist_version_model = playlist_version_model.scalar_one_or_none()
        track_model = await self.session.get(Track, input_track.track_id)

        if not playlist_version_model or not track_model:
            return None

        playlist_version_model.tracks.append(track_model)
        await self.session.flush()
        await self.session.commit()

        return SPlaylistVersionBase.model_validate(playlist_version_model, from_attributes=True)


@with_session_management
class AnalysisRepository(BaseRepository):
    async def get(self, version_id: UUID = None, task_id: UUID = None) -> SAnalysis | None:

        if version_id:
            id_query = Analysis.playlist_version_id == version_id
        elif task_id:
            id_query = Analysis.task_id == task_id
        else:
            raise ValueError('At least one of version_id or task_id must be provided')

        query = (
            select(Analysis)
            .options(
                joinedload(Analysis.playlist_version)
            )
            .where(id_query)
        )
        analysis_model = await self.session.execute(query)
        analysis_scalar = analysis_model.scalar_one_or_none()
        if not analysis_scalar:
            return None
        return SAnalysis.model_validate(analysis_scalar, from_attributes=True)

    async def create(self, input_analysis: SAnalysisBase) -> SAnalysisBase:
        analysis_model = Analysis(**input_analysis.model_dump())
        self.session.add(analysis_model)
        await self.session.flush()
        await self.session.commit()
        return SAnalysisBase.model_validate(analysis_model, from_attributes=True)

    async def update(self, analysis_id: UUID, update_data: SAnalysisUpdate) -> SAnalysis | None:
        query = select(Analysis).options(joinedload(Analysis.playlist_version)).where(Analysis.id == analysis_id)
        result = await self.session.execute(query)
        analysis_model = result.scalar_one_or_none()

        if not analysis_model:
            return None

        updatable_fields = {'status', 'uniqueness'}

        for key, value in update_data.model_dump(exclude_unset=True).items():
            if key in updatable_fields:
                setattr(analysis_model, key, value)

        await self.session.commit()
        return SAnalysis.model_validate(analysis_model, from_attributes=True)


tracks = TrackRepository()
track_features = TrackFeaturesRepository()
artists = ArtistsRepository()
playlists = PlaylistRepository()
playlist_versions = PlaylistVersionRepository()
analyzes = AnalysisRepository()
