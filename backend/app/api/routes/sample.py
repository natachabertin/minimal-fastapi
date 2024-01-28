from typing import List

from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED

from app.api.models.sample import SampleRead, SampleCreate
from app.api.services.sample import SampleCRUD
from app.db.session import DBSession, get_async_session

router = APIRouter()


@router.get("/")
async def get_all_samples() -> List[dict]:
    samples = [
        {"id": 1, "name": "Sample Route", "sample_type": "food_sample", "price": 20.05},
        {"id": 2, "name": "Sample 1", "sample_type": "paint_sample", "price": 10.05},
    ]

    return samples


@router.post(
   "",
   response_model=SampleRead,
   status_code=HTTP_201_CREATED
)
async def create_sample(
       data: SampleCreate,
       db: DBSession = Depends(get_async_session)
):
    created_sample = await SampleCRUD.create(db=db, data=data)

    return created_sample
