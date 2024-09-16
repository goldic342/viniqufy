from fastapi_async_sqlalchemy import db
from fastapi_async_sqlalchemy.exceptions import SessionNotInitialisedError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import SessionLocal


class BaseRepository:

    def __init__(self):
        self._db = db

    @property
    def session(self) -> AsyncSession:
        # Session can be taken from ``fastapi_async_sqlalchemy`` and SessionLocal.
        # Because celery is running in different python process ``db.session`` raises SessionNotInitialisedError
        # So catching it and returning SessionLocal, which is automatically closed
        # during shutdown (I guess so) - no running session are opened in pgAdmin
        try:
            return self._db.session
        except SessionNotInitialisedError:
            return SessionLocal()

    async def get(self, *args, **kwargs):
        raise NotImplementedError

    async def create(self, *args, **kwargs):
        raise NotImplementedError

    async def update(self, *args, **kwargs):
        raise NotImplementedError

    async def get_all(self, *args, **kwargs):
        raise NotImplementedError
