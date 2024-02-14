# import asyncio
# import asyncpg
# from typing import Generator
#
# import pytest, pytest_asyncio
# from httpx import AsyncClient
# from sqlalchemy.orm import sessionmaker
# from sqlmodel import SQLModel
# from sqlmodel.ext.asyncio.session import AsyncSession
#
# from app.core.config import settings
# from app.db.session import async_engine
# from app.main import app
#
#
# @pytest.fixture(scope="session")
# def event_loop(request) -> Generator:  # noqa: indirect usage
#    loop = asyncio.get_event_loop_policy().new_event_loop()
#    yield loop
#    loop.close()
#
#
# async def create_testing_database():
#     connection_url = "postgresql://postgres:postgres@localhost/postgres_test"
#     conn = await asyncpg.connect(connection_url)
#     db_name = settings.postgres_db_name
#     try:
#         # Execute SQL command to create the database
#         await conn.execute("CREATE DATABASE %(db_name)s", db_name)
#     except asyncpg.exceptions.DuplicateDatabaseError:
#         print("Database already exists")
#     finally:
#         await conn.close()
#
#
# @pytest_asyncio.fixture
# async def async_client():
#    async with AsyncClient(
#            app=app,
#            base_url="http://127.0.0.1:8000"
#    ) as client:
#       yield client
#
#
# @pytest_asyncio.fixture(scope="function")
# async def async_session() -> AsyncSession:
#     await create_testing_database()
#     session = sessionmaker(
#         async_engine, class_=AsyncSession, expire_on_commit=False
#     )
#
#     async with session() as sess:
#         async with async_engine.begin() as conn:
#             await conn.run_sync(SQLModel.metadata.create_all)
#
#         yield sess
#
#     async with async_engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.drop_all)
#
#     await async_engine.dispose()

import asyncio
import asyncpg

async def create_testing_database():
    try:
        # Establish connection to the default database
        conn = await asyncpg.connect("postgresql://postgres:postgres@localhost/postgres")
        # Execute SQL command to create the testing database
        await conn.execute("CREATE DATABASE postgres_test")
        print("Testing database created successfully")
    except asyncpg.exceptions.DuplicateDatabaseError:
        print("Database already exists")
    finally:
        await conn.close()

async def main():
    await create_testing_database()

if __name__ == "__main__":
    asyncio.run(main())