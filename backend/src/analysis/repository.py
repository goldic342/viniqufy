from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from src.analysis.models import Track, TrackFeatures, Artist
from src.analysis.schemas import STrack, STrackBase, STrackFeatures, SArtist, SArtistBase
from src.repository import BaseRepository


# TODO: find way to avoid code duplication (lazy rn)

class TrackFeaturesRepository(BaseRepository):
    async def get(self, track_id: str) -> STrackFeatures | None:
        query = (
            select(TrackFeatures)
            .options(joinedload(TrackFeatures.track))
            .where(TrackFeatures.track_id == track_id)
        )

        features_model = await self.session.execute(query)
        features_scalar = features_model.scalar_one_or_none()

        if not features_scalar:
            return None

        return STrackFeatures.model_validate(features_scalar, from_attributes=True)

    async def create(self, input_features: STrackFeatures) -> STrackFeatures:
        features_model = STrackFeatures(**input_features.model_dump())

        self.session.add(features_model)
        await self.session.flush()
        await self.session.commit()

        return STrackFeatures.model_validate(features_model, from_attributes=True)


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

    async def create(self, input_artist: SArtist) -> SArtist:
        artist_model = Artist(**input_artist.model_dump())

        self.session.add(artist_model)
        await self.session.flush()
        await self.session.commit()

        return SArtist.model_validate(artist_model, from_attributes=True)

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


class TrackRepository(BaseRepository):

    async def get(self, track_id: str) -> STrack | None:
        query = (
            select(Track)
            .options(joinedload(Track.track_features))
            .options(selectinload(Track.playlist_versions))
            .options(selectinload(Track.artists))
            .where(Track.track_id == track_id)
        )

        track_model = await self.session.execute(query)
        track_scalar = track_model.scalar_one_or_none()

        if not track_scalar:
            return None

        return STrack.model_validate(track_model.scalar(), from_attributes=True)

    async def create(self, input_track: STrack) -> STrack:
        track_model = Track(**input_track.model_dump())

        self.session.add(track_model)
        await self.session.flush()
        await self.session.commit()

        return STrack.model_validate(track_model, from_attributes=True)

    async def update(self, input_track: STrackBase) -> STrackBase:
        """
        Updating track attributes without relationships
        :param input_track: schema of track to update
        :return: updated track schema (without relationships)
        """
        track_model = await self.session.get(Track, input_track.track_id)

        for key, value in input_track.model_dump().items():
            setattr(track_model, key, value)

        await self.session.flush()
        await self.session.commit()
        return STrackBase.model_validate(track_model, from_attributes=True)

    async def set_features(self, track_id: str, features: STrackFeatures):
        track_model = await self.session.get(Track, track_id)

        if not track_model:
            return None

        track_model.track_features = TrackFeatures(**features.model_dump())
        await self.session.commit()
        return

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


tracks = TrackRepository()
track_features = TrackFeaturesRepository()
artists = ArtistsRepository()
