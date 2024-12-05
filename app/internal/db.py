from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

from .config import Config, config

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncConnection, AsyncSession, AsyncEngine

class DatabaseSessionManager:
    def __init__(self, config: Config) -> None:
        if config.db_url is None:
            raise ValueError("Database URL is not set")

        self._engine = create_async_engine(config.db_url)
        self._session_factory = async_sessionmaker(autocommit=False, bind=self._engine)
    
    @property
    def engine(self) -> Optional[AsyncEngine]:
        return self._engine

    async def close(self):
        if self._engine is None:
            raise RuntimeError("Database engine is not set")
        
        await self._engine.dispose()

        self._engine = None
        self._session_factory = None
    
    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise RuntimeError("Database engine is not set")
        
        async with self._engine.begin() as conn:
            try:
                yield conn
            finally:
                await conn.close()
                raise
    
    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._session_factory is None:
            raise RuntimeError("Database session factory is not set")
        
        session = self._session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

session_manager = DatabaseSessionManager(config)

async def get_db_session():
    async with session_manager.session() as session:
        yield session