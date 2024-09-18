import asyncio
from datetime import datetime, timedelta, date
from itertools import chain
from uuid import UUID

import numpy as np
from aiohttp import ClientSession
from scipy.stats import entropy

from src.analysis.config import analysis_settings
from src.analysis.enums import AnalysisStatus
from src.analysis.repository import playlists, playlist_versions, tracks, artists, track_features, analyzes
from src.analysis.schemas import SPlaylistCreate, SArtist, STrackFeatures, STrack, SPlaylist, SPlaylistVersionBase, \
    SPlaylistInfo, STrackBase, SArtistBase, STrackFeaturesBase, SAnalysisBase, SAnalysisUpdate, SPlaylistBase
from src.config import settings
from src.exceptions import CustomHTTPException


class AnalysisService:
    # TODO: token cache not working in different python processes (celery), token needs to be stored in file
    # NOTE: singleton pattern doesn't work because of session conflict
    API_URL = 'https://api.spotify.com/v1'
    _access_token = None
    _access_token_creation = None

    def __init__(self, client_id: str = settings.SPOTIFY_CLIENT_ID,
                 client_secret: str = settings.SPOTIFY_CLIENT_SECRET):
        self.client_id = client_id
        self.client_secret = client_secret
        self.initialized = True

    async def __aenter__(self):
        self.session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def analyze_playlist(self, playlist: SPlaylistCreate, version_id: UUID, task_id: UUID) -> float:
        # TODO: bind analysis creation to celery class
        analysis_db = await analyzes.get(version_id=version_id)

        # FIXME: Add a handler for the STARTED state to wait for the analysis to complete,
        # FIXME: then return the result once the process finishes.
        if analysis_db:
            return analysis_db.uniqueness

        analysis = await analyzes.create(
            SAnalysisBase(
                playlist_version_id=version_id,
                task_id=task_id,
                status=AnalysisStatus.STARTED)
        )

        playlist_tracks = await self.__playlist_tracks(playlist.spotify_playlist_id, version_id)
        playlist_artists = list(chain.from_iterable(track.artists for track in playlist_tracks))

        uniqueness = self.__calculate_uniqueness(playlist_tracks, playlist_artists, analysis_settings.weights)

        await analyzes.update(
            analysis.id,
            SAnalysisUpdate(
                status=AnalysisStatus.SUCCESS,
                uniqueness=uniqueness
            )
        )

        return uniqueness

    async def __set_access_token(self) -> None:
        """
        Sets the access token and its expiry time.
        """
        response = await self.session.post(
            'https://accounts.spotify.com/api/token',
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            }
        )
        if response.status != 200:
            raise Exception(f'Failed to get access token. Response status code: {response.status})')

        response_json = await response.json()
        self._access_token = response_json['access_token']
        self._access_token_creation = datetime.now()

    async def __make_auth_headers(self) -> dict:
        """
        Creates the authentication headers for the Spotify API.
        If token is expired, it will refresh it.
        :return: Headers with authentication
        """
        if not self._access_token or (datetime.now() - self._access_token_creation > timedelta(hours=1)):
            await self.__set_access_token()
        return {
            'Authorization': f"Bearer {self._access_token}"
        }

    async def __get(self, sub_url: str):
        """
        Makes a GET request to the Spotify API.
        :param sub_url: Url that follows afters https://api.spotify.com/v1
        :return: response json
        """
        if not sub_url.startswith('/'):
            raise ValueError('sub_url must start with /')

        headers = await self.__make_auth_headers()
        response = await self.session.get(f'{self.API_URL}{sub_url}', headers=headers)

        if response.status == 429:
            await asyncio.sleep(analysis_settings.rate_limit_wait)
            return await self.__get(sub_url)
        elif response.status == 404:
            raise CustomHTTPException('Spotify resource not found', status_code=404,
                                      error_code='SPOTIFY_RESOURCE_NOT_FOUND')
        elif response.status == 500:
            raise CustomHTTPException('Internal spotify server error', status_code=500,
                                      error_code='INTERNAL_SPOTIFY_ERROR')
        return await response.json()

    @staticmethod
    def __group_items(items: list[str], group_size: int = 100) -> list[str]:
        grouped_items = []

        for i in range(0, len(items), group_size):
            group = ','.join(items[i:i + group_size])
            grouped_items.append(group)

        return grouped_items

    @staticmethod
    def __get_track_date(track: dict) -> date:
        track_date: str = track['album']['release_date']
        release_date_precision: str = track['album']['release_date_precision']

        if release_date_precision != 'day':
            if release_date_precision == 'month':
                year, month = track_date.split('-')[:2]
                track_date = f'{year}-{month}-01'
            elif release_date_precision == 'year':
                track_date = f'{track_date}-01-01'

        return datetime.strptime(track_date, '%Y-%m-%d').date()

    @staticmethod
    async def __update_artist(artist_id: str, artist: dict) -> bool | SArtistBase:
        if await artists.is_expired(artist_id):
            artist_db = await artists.update(SArtistBase(
                artist_id=artist_id,
                name=artist['name'],
                genres=artist['genres'],
                popularity=artist['popularity'],
                followers=artist['followers']['total']
            ))
            return artist_db
        return False

    async def __parse_artists(self, artists_ids: list[str]) -> dict[str, SArtistBase]:
        unique_artists = list(set(artists_ids))
        grouped_artists = self.__group_items(unique_artists, group_size=50)
        artists_dict = {}

        for id_group in grouped_artists:
            response = await self.__get(f'/artists?ids={id_group}')

            for artist in response['artists']:
                artist_id = artist['id']
                artist_db = await artists.get(artist_id)

                if artist_db:
                    updated_artist = await self.__update_artist(artist_id, artist)

                    # If artist was updated, update ``artists_db``
                    if updated_artist:
                        artists_db = updated_artist
                else:
                    artist_db = await artists.create(SArtistBase(
                        artist_id=artist_id,
                        name=artist['name'],
                        genres=artist['genres'],
                        popularity=artist['popularity'],
                        followers=artist['followers']['total']
                    ))

                artists_dict[artist_id] = artist_db

        return artists_dict

    async def __parse_audio_analysis(self, tracks_ids_groups: list[str]) -> dict[str, STrackFeaturesBase]:
        audio_analysis = {}

        for group in tracks_ids_groups:
            response = await self.__get(f'/audio-features?ids={group}')

            for track_features_json in response['audio_features']:
                track_id = track_features_json['id']
                features_db = await track_features.get(track_id)

                if features_db:
                    audio_analysis[track_id] = features_db
                    continue

                audio_analysis[track_id] = STrackFeaturesBase(
                    track_id=track_id,
                    duration_ms=track_features_json['duration_ms'],
                    loudness=track_features_json['loudness'],
                    dance_ability=track_features_json['danceability'],
                    energy=track_features_json['energy'],
                    key=track_features_json['key'],
                    mode=track_features_json['mode'],
                    tempo=track_features_json['tempo'],
                    valence=track_features_json['valence']
                    # TODO: Add more params when adding more analysis data
                )

        return audio_analysis

    async def __parse_tracks(self, tracks_json: list[dict], version_id: UUID) -> list[STrack]:
        """
        Parse tracks json, loads additional data such as artist info, audio analysis and then convert to pydantic schema
        :param tracks_json: Raw tracks json (dict)
        :param version_id: Playlist version id
        :return: List of tracks as pydantic model, modified artist list and audio analysis list
        """
        result: list[STrack] = []
        artists_ids = []
        tracks_ids = []

        # Spotify API issue fix: https://github.com/spotify/web-api/issues/958
        # And removing local tracks from playlist
        cleaned_tracks = []
        for track_json in tracks_json:
            track = track_json.get('track')
            if track:
                if 'local' not in track['uri']:
                    cleaned_tracks.append(track_json)

        for track_data in cleaned_tracks:
            track = track_data.get('track')
            track_db = await tracks.get(track['id'])

            if track_db:
                if await tracks.is_expired(track_db.track_id):
                    # Almost any param can change after expiration
                    await tracks.update(STrackBase(
                        name=track['name'],
                        track_id=track['id'],  # Added because of STrackBase requires it
                        popularity=track['popularity'],
                        explicit=track['explicit'],
                        # Despite the fact that the release date should not change, we update it for security
                        release_date=self.__get_track_date(track),
                    ))

                # Artists may expire
                for artist_db in track_db.artists:
                    await self.__update_artist(artist_db.artist_id, artist_db)

                # Refreshing track_db because it may have changed
                track_db = await tracks.get(track['id'])
                result.append(track_db)

                # Skip if track is already in db
                continue

            tracks_ids.append(track['id'])

            for artist_json in track['artists']:
                artists_ids.append(artist_json['id'])

        # Removing excising in db tracks from tracks_json
        cleaned_tracks = [track for track in cleaned_tracks if track['track']['id'] in tracks_ids]

        artists_dict = await self.__parse_artists(artists_ids)
        analysis = await self.__parse_audio_analysis(self.__group_items(tracks_ids))

        for track_data in cleaned_tracks:
            track = track_data.get('track')

            track_db = await tracks.create(STrackBase(
                name=track['name'],
                track_id=track['id'],
                popularity=track['popularity'],
                explicit=track['explicit'],
                release_date=self.__get_track_date(track)
            ))

            await tracks.set_features(track_db.track_id, analysis[track_db.track_id])
            await playlist_versions.link_track(track_db, version_id)

            for artist_json in track['artists']:
                await tracks.link_artist(artists_dict[artist_json['id']], track_db.track_id)

            # Refreshing track_db because it may have changed
            track_db = await tracks.get(track['id'])
            result.append(track_db)

        return result

    async def __playlist_tracks(self, playlist_id: str, version_id: UUID, limit: int = 100, ) -> list[STrack]:
        tracks_schemas = []
        current_url = f'/playlists/{playlist_id}/tracks?limit={limit}'

        while current_url:
            response = await self.__get(current_url)

            parsed_tracks = await self.__parse_tracks(response['items'], version_id)
            tracks_schemas.extend(parsed_tracks)

            current_url = response.get('next')
            if current_url:
                current_url = current_url.split(self.API_URL)[1]

        return tracks_schemas

    @staticmethod
    async def __create_playlist_version(playlist_info: dict, playlist: SPlaylist, image_url: str) -> \
            tuple[SPlaylistInfo, UUID]:
        playlist_version = await playlist_versions.create(SPlaylistVersionBase(
            playlist_id=playlist.playlist_id,
            snapshot_id=playlist_info['snapshot_id'],
            description=playlist_info['description'],
            owner_name=playlist_info['owner']['display_name'],
            owner_spotify_id=playlist_info['owner']['id'],
            followers=playlist_info['followers']['total'],
            tracks_count=playlist_info['tracks']['total'],
            name=playlist_info['name'],
        ))

        return SPlaylistInfo.from_base_and_version(playlist, playlist_version, image_url=image_url), \
            playlist_version.version_id

    async def playlist_info(self, playlist_id: str) -> tuple[SPlaylistInfo, UUID]:
        playlist = await playlists.get(playlist_id)

        # Fields param added for reducing response time, tracks not needed
        playlist_info = await self.__get(
            f'/playlists/{playlist_id}?fields=snapshot_id,name,description,owner,followers,tracks(total),images')
        snapshot_id = playlist_info['snapshot_id']
        image_url = playlist_info.get('images')

        # array of images may be empty: https://developer.spotify.com/documentation/web-api/reference/get-playlist
        if image_url:
            image_url = image_url[0]['url']

        if playlist:
            if playlist.current_snapshot_id != snapshot_id:
                playlist_version, playlist_version_id = await self.__create_playlist_version(playlist_info, playlist,
                                                                                             image_url)
                await playlists.update(SPlaylistBase(
                    current_snapshot_id=snapshot_id,
                    spotify_playlist_id=playlist_id
                ))
                return playlist_version, playlist_version_id
            else:
                # FIXME: ERROR here idk why
                playlist_version = await playlist_versions.get(snapshot_id)
                return SPlaylistInfo.from_base_and_version(playlist, playlist_version,
                                                           image_url=image_url), playlist_version.version_id

        playlist = await playlists.create(SPlaylist(
            spotify_playlist_id=playlist_id,
            current_snapshot_id=snapshot_id
        ))

        playlist_version, playlist_version_id = await self.__create_playlist_version(playlist_info, playlist, image_url)

        return playlist_version, playlist_version_id

    async def __track_info(self, track_id: str):
        return await self.__get(f'/tracks/{track_id}')

    async def __track_audio_analysis(self, track_id: str):
        response = await self.__get(f'/audio-features/{track_id}')
        return STrackFeatures(
            track_id=track_id,
            duration_ms=response['duration_ms'],
            loudness=response['loudness'],
            dance_ability=response['danceability'],
            energy=response['energy'],
            key=response['key'],
            mode=response['mode'],
            tempo=response['tempo'],
            valence=response['valence']
        )

    async def __artist_info(self, artist_id: str):
        return await self.__get(f'/artists/{artist_id}')

    @staticmethod
    def __data_set_uniqueness(values: list[int | float]) -> float:
        """
        Calculating the uniqueness of data based on Shannon index, Simpson index, and coefficient of variation.

        :param data (array-like): Input data (list, array or pandas series).

        :return: Data uniqueness value (from 0 to 1).
        """

        if len(values) == 0:
            return 0.0

        data_array = np.array(values)

        # Calculate Shannon index
        unique, counts = np.unique(data_array, return_counts=True)
        probabilities = counts / len(data_array)
        shannon_index = entropy(probabilities, base=2)

        # Normalize Shannon index (from 0 to 1)
        max_shannon_index = np.log2(len(unique))
        normalized_shannon_index = shannon_index / max_shannon_index if max_shannon_index > 0 else 0

        # Calculate Simpson index
        simpson_index = np.sum(probabilities ** 2)

        # Normalize Simpson index (from 0 to 1), the higher the value (1 - D), the higher the diversity
        normalized_simpson_index = 1 - simpson_index

        # Calculate coefficient of variation
        mean_value = np.mean(data_array)
        std_dev = np.std(data_array)
        coefficient_of_variation = std_dev / mean_value if mean_value != 0 else 0

        # Normalize coefficient of variation (from 0 to 1)
        # For this example, we assume CV > 1 as 1 (very high variability)
        normalized_cv = min(coefficient_of_variation, 1)

        # Combine the three indicators to obtain uniqueness
        uniqueness_score = (normalized_shannon_index + normalized_simpson_index + normalized_cv) / 3

        return uniqueness_score

    def __calculate_uniqueness(self, playlist_tracks: list[STrack], playlist_artists: list[SArtist],
                               weights: dict[str, int]) -> float:
        """
        Calculates the uniqueness of a playlist based on the popularity of tracks, artists, variety of genres,
        variety of tracks audio params

        U = (W1 * P + W2 * A + W3 * M + W4 * G + W5 * T + W6 * E) / (W1 + W2 + W3 + W4 + W5 + W6)
        where:

        U - overall uniqueness score of the playlist (from 0 to 1)
        W1, W2, ..., W6 - weights for each component

        Components:

        P - Popularity:
        P = 1 - ((p_tracks + p_artists) / 200)
            p_tracks - average popularity of tracks
            p_artists - average popularity of artists

        A - Artist Diversity:
        A = (d / t) * (1 - (f / t))
            d - number of unique artists
            t - total number of tracks
            f - number of tracks of the most frequent artist

        M - Musical Diversity:
        M = (Dt + Dk + Dl + Dd + Dm + De + Dv + Dda) / 8
            Dt - tempo diversity
            Dk - key diversity
            Dl - loudness diversity
            Dd - duration diversity
            Dm - mode diversity (major/minor)
            De - energy diversity
            Dv - valence diversity (mood)
            Dda - dance-ability diversity

        G - Genre Diversity:
        G = (g / t) * (1 - (H / log(g)))
            g - number of unique genres
            t - total number of tracks
            H - Shannon index for genre distribution

        T - Temporal Diversity:
        T = 1 - (max(y) - min(y)) / (current_year - min(y))
            y - years of track releases
            current_year - current year

        E - Era Diversity:
        E = summ(1 / count_playlists_with_track) / t
            t - total number of tracks

        :param playlist_tracks: List of SpotifyTrack objects
        :param playlist_artists: List of SpotifyArtist objects
        :param weights: Dictionary of weights
        :return: Uniqueness score between 0 and 1
        """
        # TODO: Add edge cases handing such as one genre

        # Weights
        w1 = weights.get('popularity')
        w2 = weights.get('artist_diversity')
        w3 = weights.get('musical_diversity')
        w4 = weights.get('genre_diversity')
        w5 = weights.get('temporal_diversity')
        w6 = weights.get('era_diversity')
        w_list = [w1, w2, w3, w4, w5, w6]

        # Weights validation
        if any(param is None for param in w_list):
            raise ValueError('Not all weights are set.')

        if sum(w_list) != 1:
            raise ValueError('Sum of weights must be equal to 1')

        # 1. Popularity (P)
        p_tracks = np.mean([track.popularity for track in playlist_tracks])
        p_artists = np.mean([artist.popularity for artist in playlist_artists])
        P = 1 - ((p_tracks + p_artists) / 200)

        # 2. Artist Diversity (A)
        unique_artists = len(set(artist.artist_id for track in playlist_tracks for artist in track.artists))
        artist_counts = np.array([len(track.artists) for track in playlist_tracks])
        A = (unique_artists / len(playlist_tracks)) * (1 - (np.max(artist_counts) / len(playlist_tracks)))

        # 3. Musical Diversity (M)
        tempos = [track.track_features.tempo for track in playlist_tracks]
        keys = [track.track_features.key for track in playlist_tracks]
        loudness = [track.track_features.loudness for track in playlist_tracks]
        durations = [track.track_features.duration_ms for track in playlist_tracks]
        modes = [track.track_features.mode for track in playlist_tracks]
        energies = [track.track_features.energy for track in playlist_tracks]
        valences = [track.track_features.valence for track in playlist_tracks]
        danceabilities = [track.track_features.dance_ability for track in playlist_tracks]

        M = np.mean([
            self.__data_set_uniqueness(tempos),
            self.__data_set_uniqueness(keys),
            self.__data_set_uniqueness(loudness),
            self.__data_set_uniqueness(durations),
            self.__data_set_uniqueness(modes),
            self.__data_set_uniqueness(energies),
            self.__data_set_uniqueness(valences),
            self.__data_set_uniqueness(danceabilities)
        ])

        # 4. Genre Diversity (G)
        genres = list(chain.from_iterable(artist.genres for artist in playlist_artists))
        unique_genres = len(set(genres))
        genre_counts = np.array([genres.count(genre) for genre in set(genres)])
        H = -np.sum((genre_counts / len(genres)) * np.log(genre_counts / len(genres)))
        G = (unique_genres / len(playlist_tracks)) * (1 - (H / np.log(unique_genres)))

        # 5. Temporal Diversity (T)
        release_dates = [track.release_date for track in playlist_tracks]  # track.release_date in date format
        current_date = datetime.now().date()
        years = [t_date.year for t_date in release_dates]
        min_year = min(years)
        T = 1 - (max(years) - min_year) / (current_date.year - min_year + 1)  # Adding 1 to avoid division by zero

        # 6. Era Diversity (E)
        eras = [year // 10 for year in years]  # Defining eras as decades
        current_era = current_date.year // 10
        min_era = min_year // 10
        E = len(set(eras)) / (current_era - min_era + 1)

        # Calculate final uniqueness score
        U = (w1 * P + w2 * A + w3 * M + w4 * G + w5 * T + w6 * E) / (w1 + w2 + w3 + w4 + w5 + w6)

        return U
