from fastapi_async_sqlalchemy import db
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:

    def __init__(self):
        self._db = db

    @property
    def session(self) -> AsyncSession:
        return self._db.session

    async def get(self, *args, **kwargs):
        raise NotImplementedError

    async def create(self, *args, **kwargs):
        raise NotImplementedError

    async def update(self, *args, **kwargs):
        raise NotImplementedError

    async def get_all(self, *args, **kwargs):
        raise NotImplementedError
