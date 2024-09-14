from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base

from src.config import settings

Base = declarative_base()
engine = create_async_engine(
    settings.ASYNC_DATABASE_URI,
    poolclass=NullPool,  # Maybe will be changed later
    pool_size=5,
    max_overflow=10,
)
