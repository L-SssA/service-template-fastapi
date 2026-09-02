from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from app.config import config


engine: AsyncEngine = create_async_engine(
    config.sql_url,
    echo=True if config.log_level == "debug" else False,
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
