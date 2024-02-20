from typing import List

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.api.models.sample import SampleRead, SampleCreate
from app.api.services.sample import SampleCRUD
from app.db.session import get_async_session


router = APIRouter()


@router.get("", name="samples:get-samples")
async def get_all_samples() -> List[dict]:
    samples = [
        {"id": 1, "name": "Sample Route", "sample_type": "food_sample", "price": 20.05},
        {"id": 2, "name": "Sample 1", "sample_type": "paint_sample", "price": 10.05},
    ]

    return samples


@router.post(
    "",
    response_model=SampleRead,
    status_code=HTTP_201_CREATED,
    name="samples:create-sample"
)
async def create_sample(
       data: SampleCreate,
       db: AsyncSession = Depends(get_async_session)
):
    created_sample = await SampleCRUD(db=db).create(data=data)

    return created_sample
