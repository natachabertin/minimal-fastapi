from typing import List

from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def get_all_samples() -> List[dict]:
    samples = [
        {"id": 1, "name": "Sample Route", "sample_type": "food_sample", "price": 20.05},
        {"id": 2, "name": "Sample 1", "sample_type": "paint_sample", "price": 10.05},
    ]

    return samples
