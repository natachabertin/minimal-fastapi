import pytest
from httpx import AsyncClient

from app.main import app


class TestRoot:
    route = app.url_path_for("root")
    @pytest.mark.asyncio
    async def test_get_root(
        self,
        async_client: AsyncClient
    ):
       response = await async_client.get(self.route)

       assert response.json() ==  {'message': 'Hello World'}
       assert response.status_code == 200
