import asyncio
from copy import deepcopy
from datetime import datetime, timedelta
from itertools import chain

import numpy as np
from aiohttp import ClientSession
from scipy.stats import entropy

from config import WEIGHTS, RATE_LIMIT_WAIT
from schemas import SpotifyPlaylistStart, SpotifyTrack, SpotifyArtist, SpotifyTrackAnalysis


class SpotifyService:
    # TODO: Add token caching, so all instances of class have the same token
    API_URL = 'https://api.spotify.com/v1'
    access_token = None
    access_token_creation = None

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret

    async def __aenter__(self):
        self.session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def get_uniqueness(self, playlist: SpotifyPlaylistStart) -> float:
        tracks = await self.__playlist_tracks(playlist.spotify_id)
        artists = list(chain.from_iterable(track.artists for track in tracks))

        return await self.__calculate_uniqueness(tracks, artists, WEIGHTS)

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

        self.access_token = response_json['access_token']
        self.access_token_creation = datetime.now()

    async def __make_auth_headers(self) -> dict:
        """
        Creates the authentication headers for the Spotify API.
        If token is expired, it will refresh it.
        :return: Headers with authentication
        """
        if not self.access_token or datetime.now() - self.access_token_creation > timedelta(hours=1):
            await self.__set_access_token()

        return {
            'Authorization': f"Bearer {self.access_token}"
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
            await asyncio.sleep(RATE_LIMIT_WAIT)
            return await self.__get(sub_url)

        return await response.json()

    async def __parse_tracks(self,
                             tracks: dict,
                             parsed_artists: list[SpotifyArtist],
                             parsed_audio_analysis: list[SpotifyTrackAnalysis]) -> \
            tuple[list[SpotifyTrack], list[SpotifyArtist], list[SpotifyTrackAnalysis]]:
        """
        Parse tracks json, loads additional data such as artist info, audio analysis and then convert to pydantic schema
        :param tracks: Raw tracks json (dict)
        :param parsed_artists: List of already parsed SpotifyArtist instances
        :param parsed_audio_analysis: List of already parsed SpotifyTrackAnalysis instances
        :return: List of tracks as pydantic model, modified artist list and audio analysis list
        """
        result: list[SpotifyTrack] = []

        # To prevent mutations
        parsed_artists_copy = deepcopy(parsed_artists)
        parsed_audio_analysis_copy = deepcopy(parsed_audio_analysis)

        for track_data in tracks:
            track = track_data['track']
            artists = []

            for artist in track['artists']:
                existing_artist = next((a for a in parsed_artists_copy if a.spotify_id == artist['id']), None)
                if existing_artist:
                    artists.append(existing_artist)
                    continue

                artist_info = await self.__artist_info(artist['id'])
                artist_schema = SpotifyArtist(
                    name=artist_info['name'],
                    spotify_id=artist_info['id'],
                    genres=artist_info['genres'],
                    popularity=artist_info['popularity'],
                )
                artists.append(artist_schema)
                parsed_artists_copy.append(artist_schema)

            audio_analysis = next(
                (analysis for analysis in parsed_audio_analysis_copy if analysis.spotify_id == track['id']), None)
            if not audio_analysis:
                audio_analysis = await self.__track_audio_analysis(track['id'])
                parsed_audio_analysis_copy.append(audio_analysis)

            result.append(SpotifyTrack(
                name=track['name'],
                spotify_id=track['id'],
                popularity=track['popularity'],
                release_year=track['album']['release_date'].split('-')[0],
                artists=artists,
                analysis=audio_analysis
            ))

        return result, parsed_artists_copy, parsed_audio_analysis_copy

    async def __playlist_tracks(self, playlist_id: str, limit: int = 30) -> list[SpotifyTrack]:
        tracks = []
        current_url = f'/playlists/{playlist_id}/tracks?limit={limit}'

        artists = []
        audio_analysis = []

        while current_url:
            response = await self.__get(current_url)

            parsed_tracks, artists, audio_analysis = await self.__parse_tracks(
                response['items'],
                artists,
                audio_analysis
            )

            tracks.extend(parsed_tracks)

            current_url = response.get('next')
            if current_url:
                current_url = current_url.split(self.API_URL)[1]

        return tracks

    async def __playlist_info(self, playlist_id: str):
        return await self.__get(f'/playlists/{playlist_id}')

    async def __track_info(self, track_id: str):
        return await self.__get(f'/tracks/{track_id}')

    async def __track_audio_analysis(self, track_id: str):
        response = await self.__get(f'/audio-features/{track_id}')
        return SpotifyTrackAnalysis(
            spotify_id=track_id,
            duration=response['duration_ms'],
            loudness=response['loudness'],
            danceability=response['danceability'],
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

    async def __calculate_uniqueness(self, tracks: list[SpotifyTrack], artists: list[SpotifyArtist],
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

        :param tracks: List of SpotifyTrack objects
        :param artists: List of SpotifyArtist objects
        :param weights: Dictionary of weights
        :return: Uniqueness score between 0 and 1
        """

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
        p_tracks = np.mean([track.popularity for track in tracks])
        p_artists = np.mean([artist.popularity for artist in artists])
        P = 1 - ((p_tracks + p_artists) / 200)

        # 2. Artist Diversity (A)
        unique_artists = len(set(artist.spotify_id for track in tracks for artist in track.artists))
        artist_counts = np.array([len(track.artists) for track in tracks])
        A = (unique_artists / len(tracks)) * (1 - (np.max(artist_counts) / len(tracks)))

        # 3. Musical Diversity (M)
        tempos = [track.analysis.tempo for track in tracks]
        keys = [track.analysis.key for track in tracks]
        loudness = [track.analysis.loudness for track in tracks]
        durations = [track.analysis.duration for track in tracks]
        modes = [track.analysis.mode for track in tracks]
        energies = [track.analysis.energy for track in tracks]
        valences = [track.analysis.valence for track in tracks]
        danceabilities = [track.analysis.danceability for track in tracks]

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
        genres = list(chain.from_iterable(artist.genres for artist in artists))
        unique_genres = len(set(genres))
        genre_counts = np.array([genres.count(genre) for genre in set(genres)])
        H = -np.sum((genre_counts / len(genres)) * np.log(genre_counts / len(genres)))
        G = (unique_genres / len(tracks)) * (1 - (H / np.log(unique_genres)))

        # 5. Temporal Diversity (T)
        years = [track.release_year for track in tracks]
        current_year = datetime.now().year
        T = 1 - (max(years) - min(years)) / (current_year - min(years) + 1)  # Adding 1 to avoid division by zero

        # 6. Era Diversity (E)
        eras = [year // 10 for year in years]  # Defining eras as decades
        E = len(set(eras)) / ((current_year // 10) - (min(years) // 10) + 1)

        # Calculate final uniqueness score
        U = (w1 * P + w2 * A + w3 * M + w4 * G + w5 * T + w6 * E) / (w1 + w2 + w3 + w4 + w5 + w6)

        return U
