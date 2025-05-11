from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from collections.abc import AsyncGenerator


# engine = create_async_engine("sqlite+aiosqlite:///test.db", echo=True)
engine = create_async_engine("postgresql+asyncpg://oleg:oleg@127.0.0.1:5432/oleg", echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

engine = create_async_engine("postgresql+asyncpg://tamam:Kdwo28k7s02wkKh!@127.0.0.1:5432/monitoractivity", echo=False)
class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with async_session_maker() as session:
        yield session
