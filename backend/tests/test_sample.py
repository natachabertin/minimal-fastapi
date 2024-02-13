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


@pytest.mark.asyncio
async def test_get_all_samples(
       async_client: AsyncClient,
       async_session: AsyncSession
):
   response = await async_client.get("/sample")

   assert response.json() ==  [
        {"id": 1, "name": "Sample Route", "sample_type": "food_sample", "price": 20.05},
        {"id": 2, "name": "Sample 1", "sample_type": "paint_sample", "price": 10.05},
    ]
   assert response.status_code == 200



@pytest.mark.asyncio
async def test_post_sample(
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
