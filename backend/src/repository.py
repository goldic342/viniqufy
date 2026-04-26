from sqlalchemy.ext.asyncio import AsyncSession

from src.database import SessionLocal


class BaseRepository:
    async def __aenter__(self):
        self.session = SessionLocal()

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.close()

    def __init__(self):
        self.session: AsyncSession = None  # type: ignore

    async def get(self, *args, **kwargs):
        raise NotImplementedError

    async def create(self, *args, **kwargs):
        raise NotImplementedError

    async def update(self, *args, **kwargs):
        raise NotImplementedError

    async def get_all(self, *args, **kwargs):
        raise NotImplementedError
