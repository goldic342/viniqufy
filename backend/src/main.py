from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from analysis.router import router

from config import settings

from loguru import logger

settings.DATA_DIR.mkdir(exist_ok=True)
settings.LOG_DIR.mkdir(exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting backend...")
    yield
    logger.info("Stopping backend...")


app = FastAPI(
    docs_url=None if settings.IS_PROD else "/docs",
    redoc_url=None if settings.IS_PROD else "/redoc",
    openapi_url=None if settings.IS_PROD else "/openapi.json",
    lifespan=lifespan,
)

app.include_router(router)

origins = [o.strip() for o in settings.ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.add(
    settings.LOG_DIR / "viniqufy.log",
    level="INFO" if settings.IS_PROD else "DEBUG",
    compression="gz",
    rotation="1 week",
    retention="2 weeks",
    backtrace=True,
    diagnose=True,
    format=(
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | "
        "{name}:{function}:{line} - {message} | {extra}"
    ),
)
