import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_get_sample(
       async_client: AsyncClient,
       async_session: AsyncSession
):
   response = await async_client.get("/sample")

   assert response.status_code == 200

   resp = response.json() is not None
