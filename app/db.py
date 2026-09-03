from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import config
from app.modules import load_models


async_engine: AsyncEngine = create_async_engine(
    config.sql_url,
    echo=True if config.log_level == "debug" else False,
)

async def init_db():
    async with async_engine.begin() as conn:
        load_models()
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with Session() as session:
        yield session
