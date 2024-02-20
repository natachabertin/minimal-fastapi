import pytest

from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession


class TestSampleRoutes:
    @pytest.mark.asyncio
    async def test_get_all_samples(
        self,
        app: FastAPI,
        async_client: AsyncClient
    ) -> None:

        route = app.url_path_for("samples:get-samples")
        response = await async_client.get(route)

        assert response.json() ==  [
             {"id": 1, "name": "Sample Route", "sample_type": "food_sample", "price": 20.05},
             {"id": 2, "name": "Sample 1", "sample_type": "paint_sample", "price": 10.05},
        ]
        assert response.status_code == 200


    @pytest.mark.asyncio
    async def test_post_sample(
        self,
        app: FastAPI,
        async_client: AsyncClient,
        async_session: AsyncSession
    ):
        payload = {
            "name": "some name",
            "sample_type": "paint",
            "price": 10
        }
        response = await async_client.post(
            "/sample", json=payload
        )

        assert response.json() == {
            'name': 'some name',
            'sample_type': 'paint',
            'price': 10.0
        }
        assert response.status_code == 201


    @pytest.mark.asyncio
    async def test_post_sample_error(
        self,
        app: FastAPI,
        async_client: AsyncClient,
        async_session: AsyncSession
    ):
       response = await async_client.post("/sample")

       assert response.json() == {'detail': [{'input': None,
                 'loc': ['body'],
                 'msg': 'Field required',
                 'type': 'missing',
                 'url': 'https://errors.pydantic.dev/2.5/v/missing'}]}
       assert response.status_code == 422
