import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_get_root(
       async_client: AsyncClient,
       async_session: AsyncSession
):
   response = await async_client.get("/")

   assert response.json() ==  {'message': 'Hello World'}
   assert response.status_code == 200
