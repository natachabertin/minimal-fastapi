import asyncio
from typing import Generator

import pytest, pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings
from app.db.session import async_engine

from app.main import app


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:  # noqa: indirect usage
   loop = asyncio.get_event_loop_policy().new_event_loop()
   yield loop
   loop.close()


@pytest_asyncio.fixture
async def async_client():
   async with AsyncClient(
           app=app,
           base_url=f"http://{settings.api_prefix}"
   ) as client:
      yield client


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncSession:
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
