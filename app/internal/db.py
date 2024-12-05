from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional

from .config import Config, config

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncConnection, AsyncSession, AsyncEngine

class DatabaseSessionManager:
    """
    Gerenciador de sessões assíncronas do banco de dados.
    Tem como objetivo agir como um adaptador para o FastAPI para prover
    sessões on-demand para as rotas conforme forem solicitadas pelas 
    requisições.
    """

    def __init__(self, config: Config) -> None:
        if config.db_url is None:
            raise ValueError("Database URL is not set")

        self._engine = create_async_engine(config.db_url)
        self._session_factory = async_sessionmaker(autocommit=False, bind=self._engine)
    
    @property
    def engine(self) -> Optional[AsyncEngine]:
        return self._engine

    async def close(self):
        """
        Encerra a sessão assíncrona do banco de dados
        """
        if self._engine is None:
            raise RuntimeError("Database engine is not set")
        
        await self._engine.dispose()

        self._engine = None
        self._session_factory = None
    
    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """
        @requires: self._engine

        Realiza uma conexão assíncrona com o banco de dados e
        a finaliza ao final da operação.
        """
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
        """
        @requires: self._session_factory

        Realiza uma sessão assíncrona com o banco de dados e
        a finaliza ao final da operação.

        Realiza rollback em caso de exception.
        """
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
    """
    Cria uma seção assíncrona para o banco de dados para 
    uma operação e a finaliza ao final da mesma.
    """
    async with session_manager.session() as session:
        yield session