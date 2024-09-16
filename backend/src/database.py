from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from src.config import settings

Base = declarative_base()
engine = create_async_engine(str(settings.ASYNC_DATABASE_URI), echo=settings.DEBUG_MODE)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
