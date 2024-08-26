from datetime import datetime, timedelta

from aiohttp import ClientSession

from schemas import SpotifyPlaylistCreate


class SpotifyService:
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
        # Get playlist info > get tracks info > calculate uniqueness
        pass

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

    async def __playlist_info(self, playlist_id: str):
        pass

    async def __track_info(self, track_id: str):
        pass

    async def __calculate_uniqueness(self):
        pass
