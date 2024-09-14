from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware

from database import engine
from src.analysis.router import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SQLAlchemyMiddleware,
    engine=engine,  # Custom engine, params set in database.py
)

app.include_router(router)
