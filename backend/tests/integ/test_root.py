import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_root(
       async_client: AsyncClient
):
   response = await async_client.get("/")

   assert response.json() ==  {'message': 'Hello World'}
   assert response.status_code == 200
