import asyncio
import math
from collections import Counter
from datetime import datetime, timedelta
from statistics import mean

from aiohttp import ClientSession

from schemas import SpotifyPlaylistCreate, SpotifyTrack, SpotifyArtist, SpotifyTrackBase, SpotifyTrackAnalysis


class SpotifyService:
    # TODO: Add token caching, so all instances of class have the same token
    API_URL = 'https://api.spotify.com/v1'
    access_token = None
    access_token_creation = None

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = None

    async def __aenter__(self):
        self.session = ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def get_uniqueness(self, playlist: SpotifyPlaylistCreate):
        # TODO: Add saving to database: playlist info
        tracks_base = await self.__playlist_tracks(playlist.spotify_id)

        tracks = []
        artists = []

        for track in tracks_base:
            tracks.append(SpotifyTrack(**track.dict(), analysis=await self.__track_audio_analysis(track.spotify_id)))
            artists.extend(track.artists)

        print(tracks)
        print(artists)

        return await self.__calculate_uniqueness(tracks, artists)

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
        return await response.json()

    async def __parse_tracks(self, tracks: dict) -> list[SpotifyTrackBase]:
        """
        Parse tracks json, loads additional data and then convert to pydantic schema.
        :param tracks: Raw tracks json (dict)
        :return: List of tracks as pydantic model
        """
        result = []

        for track in tracks:
            track = track['track']
            artists = []

            for artist in track['artists']:
                artist_info = await self.__artist_info(artist['id'])
                artists.append(SpotifyArtist(
                    name=artist_info['name'],
                    spotify_id=artist_info['id'],
                    genres=artist_info['genres'],
                    popularity=artist_info['popularity'],
                ))

            result.append(SpotifyTrackBase(
                name=track['name'],
                spotify_id=track['id'],
                popularity=track['popularity'],
                artists=artists,
            ))

        return result

    async def __playlist_tracks(self, playlist_id: str, limit: int = 30) -> list[SpotifyTrackBase]:
        tracks = []
        next_url = f'/playlists/{playlist_id}/tracks?limit={limit}'

        while True:
            response = await self.__get(next_url)
            tracks.extend(await self.__parse_tracks(response['items']))

            if response['next']:
                next_url = response['next']
            else:
                break

        return tracks

    async def __playlist_info(self, playlist_id: str):
        return await self.__get(f'/playlists/{playlist_id}')

    async def __track_info(self, track_id: str):
        return await self.__get(f'/tracks/{track_id}')

    async def __track_audio_analysis(self, track_id: str):
        response = await self.__get(f'/audio-analysis/{track_id}')
        return SpotifyTrackAnalysis(**response['track'])

    async def __artist_info(self, artist_id: str):
        return await self.__get(f'/artists/{artist_id}')

    @staticmethod
    async def __calculate_uniqueness(tracks: list[SpotifyTrack], artists: list[SpotifyArtist]):
        def calculate_diversity(values) -> float:
            """
            Calculates diversity for numerical parameters using coefficient of variation.

            :param values: List of numerical values
            :return: Normalized diversity value from 0 to 1
            """
            mean_values = mean(values)  # Mean value
            # Standard deviation
            std_dev = math.sqrt(sum((x - mean_values) ** 2 for x in values) / len(values))
            cv = std_dev / abs(mean_values) if mean_values != 0 else 0  # Coefficient of variation
            return cv / (cv + 1)  # Normalize the result

        def calculate_shannon_diversity(values):
            """
            Calculates Shannon entropy for categorical parameters.

            :param values: List of categorical values
            :return: Normalized Shannon entropy from 0 to 1
            """
            counter = Counter(values)  # Counting frequency of each value
            total = sum(counter.values())  # Total count of values
            # Calculating probabilities for each unique value
            probabilities = [count / total for count in counter.values()]
            # Calculating Shannon entropy
            h = -sum(p * math.log(p) for p in probabilities if p > 0)
            # Normalizing by maximum possible diversity
            return h / math.log(len(counter))

        # 1. Calculating basic params
        p = mean(track.popularity for track in tracks)  # Avg popularity of tracks
        a = mean(artist.popularity for artist in artists)  # Avg popularity of artists
        d = len(set(artist.spotify_id for artist in artists))  # Count of unique artists
        t = len(tracks)  # Total count of tracks

        # 2. Calculating musical parameters
        tempos = [track.analysis.tempo for track in tracks]
        keys = [track.analysis.key for track in tracks]
        modes = [track.analysis.mode for track in tracks]
        loudness = [track.analysis.loudness for track in tracks]
        durations = [track.analysis.duration for track in tracks]

        tempo_diversity = calculate_diversity(tempos)
        key_diversity = calculate_shannon_diversity(keys)
        loudness_diversity = calculate_diversity(loudness)
        duration_diversity = calculate_diversity(durations)

        # For the mode (major/minor), we use a simple ratio
        mode_diversity = min(modes.count(0), modes.count(1)) / max(modes.count(0), modes.count(1))

        # 3. Calculating collaboration diversity
        max_artists_per_track = max(len(track.artists) for track in tracks)
        collab_diversity = 1  # If no collaborations, diversity is 1

        if max_artists_per_track > 1:
            tracks_with_collabs = [len(track.artists) - 1 for track in tracks if len(track.artists) > 1]
            avg_collabs_per_track = mean(tracks_with_collabs)

            collab_diversity = (avg_collabs_per_track / (max_artists_per_track - 1)) * (
                    len(tracks_with_collabs) / len(tracks))

        # Calculating the final uniqueness
        uniqueness = (
                (1 - p / 100) *  # Track popularity factor
                (1 - a / 100) *  # Artist popularity factor
                (1 - d / t) *  # Artist diversity factor
                (1 - tempo_diversity) *  # Tempo diversity factor
                (1 - key_diversity) *  # Key diversity factor
                (1 - mode_diversity) *  # Mode diversity factor
                (1 - loudness_diversity) *  # Loudness diversity factor
                (1 - duration_diversity) *  # Duration diversity factor
                collab_diversity *  # Collaboration diversity factor
                100  # Convert to percents
        )

        return uniqueness