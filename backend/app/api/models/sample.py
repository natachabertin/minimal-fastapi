from enum import Enum
from typing import Optional

from sqlmodel import SQLModel

from app.api.models.core import UUIDMixin, AuditMixin


class SampleType(str, Enum):
    food_sample = "food"
    paint_sample = "paint"
    fabric_sample = "fabric"
    cosmetic_sample = "cosmetic"


class SampleBase(SQLModel):
    """Common properties to all Sample models."""
    name: str
    sample_type: Optional[SampleType] = SampleType.food_sample
    price: Optional[float] = 0.0


class SampleDB(UUIDMixin, SampleBase, AuditMixin, table=True):
    __tablename__ = "samples"

    name: str
    sample_type: SampleType
    price: float


class SampleRead(SampleBase):
    pass


class SampleCreate(SampleBase):
    name: str
    price: float


class SampleUpdate(SampleBase):
    sample_type: Optional[str]
