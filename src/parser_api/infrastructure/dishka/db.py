

from dishka import Provider, provide, Scope
from typing import AsyncIterable
from contextlib import asynccontextmanager 
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, AsyncSession, create_async_engine

from parser_api.infrastructure.config import DatabaseConfig
from parser_api.infrastructure.db.uow import UnitOfWork


class DatabaseProvider(Provider):
    scope = Scope.APP 

    @provide
    async def get_engine(self, config: DatabaseConfig) -> AsyncIterable[AsyncEngine]:
        print(config, 'DB')
        #print("get_engine: Creating engine...")
        engine = create_async_engine(config.build_connection_url())
        try:
            yield engine
        finally:
            #print("get_engine: Disposing engine...")
            await engine.dispose(True)

    @provide
    async def get_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        #print("get_pool: Creating sessionmaker pool...")
        return async_sessionmaker(engine, expire_on_commit=False)
    
    @provide(scope=Scope.REQUEST)

    async def get_session(self, pool: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        #print("get_session: Getting session from pool...")
        async with pool() as session:
            try:
                yield session
            finally:
                #print("get_session: Closing session...")
                pass

    uow = provide(UnitOfWork, scope=Scope.REQUEST)
