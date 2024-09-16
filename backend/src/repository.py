import functools
import inspect

from fastapi_async_sqlalchemy import db
from fastapi_async_sqlalchemy.exceptions import SessionNotInitialisedError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import SessionLocal


def with_session_management(cls):
    class SessionManager:
        def __init__(self):
            self._session = None

        async def __aenter__(self):
            try:
                self._session = db.session
            except SessionNotInitialisedError:
                self._session = SessionLocal()
            return self._session

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            try:
                # Not closing session if it session from ``fastapi_async_sqlalchemy``
                db.session
            except SessionNotInitialisedError:
                await self._session.close()
                self._session = None

    def wrap_method(original_method):
        @functools.wraps(original_method)
        async def wrapper(self, *args, **kwargs):
            async with SessionManager() as session:
                self._session = session
                try:
                    return await original_method(self, *args, **kwargs)
                finally:
                    self._session = None

        return wrapper

    for name, method in inspect.getmembers(cls, inspect.iscoroutinefunction):
        # For methods that don't need sqlalchemy session
        if not name.startswith('__'):
            setattr(cls, name, wrap_method(method))

    return cls


class BaseRepository:
    _session: AsyncSession | None

    def __init__(self):
        self._db = db

    @property
    def session(self) -> AsyncSession:
        if not hasattr(self, '_session') or self._session is None:
            raise RuntimeError(
                "Session is not initialized. This should not happen if using the @with_session_management decorator.")
        return self._session

    async def get(self, *args, **kwargs):
        raise NotImplementedError

    async def create(self, *args, **kwargs):
        raise NotImplementedError

    async def update(self, *args, **kwargs):
        raise NotImplementedError

    async def get_all(self, *args, **kwargs):
        raise NotImplementedError
