import os

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, \
    AsyncSession

engine = create_async_engine(
    os.environ['db_uri'],
    isolation_level='REPEATABLE READ',
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
