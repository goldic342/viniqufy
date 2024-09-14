from fastapi_async_sqlalchemy import db
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:

    def __init__(self):
        self.session: AsyncSession = db.session

    async def get(self, *args, **kwargs):
        raise NotImplementedError

    async def create(self, *args, **kwargs):
        raise NotImplementedError

    async def update(self, *args, **kwargs):
        raise NotImplementedError

    async def get_all(self, *args, **kwargs):
        raise NotImplementedError
