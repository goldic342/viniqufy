from schemas import SpotifyPlaylistCreate


class SpotifyService:
    async def get_uniqueness(self, playlist: SpotifyPlaylistCreate):
        # Get playlist info > get tracks info > calculate uniqueness
        pass

    async def __playlist_info(self, playlist_id: str):
        pass
    
    async def __track_info(self, track_id: str):
        pass

    async def __calculate_uniqueness(self):
        pass
