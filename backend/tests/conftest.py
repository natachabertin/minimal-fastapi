import asyncpg
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.session import async_engine
from app.main import app


async def create_testing_database():
    """
    WARN: This is a challenge non prod project; so, in order to create the test db on start,
    it connects to postgres standard DB (in here, prod db) and creates the test db in the next line.

    If you use this code in a productive CI/CD, you may wanna change the way the DB is created.
    You may not have permissions to connect to prod DB and create another DB from there.
    You should go further and create a user with permissions first,
    or just create a blank DB_test in a previous step in makefile test command.
    """
    try:
        conn = await asyncpg.connect("postgresql://postgres:postgres@localhost/postgres")
        await conn.execute("CREATE DATABASE postgres_test")
        print("Testing database created successfully")
    except asyncpg.exceptions.DuplicateDatabaseError:
        print("Database already exists")
    finally:
        await conn.close()


@pytest_asyncio.fixture
async def async_client():
   async with AsyncClient(
           app=app,
           base_url="http://127.0.0.1:8000"
   ) as client:
      yield client


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncSession:
    await create_testing_database()
    session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session() as sess:
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        yield sess

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

    await async_engine.dispose()
