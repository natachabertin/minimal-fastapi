from enum import Enum
from typing import Optional

from sqlalchemy import event
from sqlmodel import SQLModel, Enum

from app.api.models.core import UUIDMixin, AuditMixin


class SampleType(str, Enum):
    food_sample = "food"
    paint_sample = "paint"
    fabric_sample = "fabric"
    cosmetic_sample = "cosmetic"


@event.listens_for(SQLModel.metadata, "before_create")
def _create_enums(metadata, conn, **kw):  # noqa: indirect usage
    """
    Ensure enums are created before continuing with the tables.
    This helps on test DB creation.
    """
    SampleType.create(conn, checkfirst=True)


class SampleBase(SQLModel):
    """Common properties to all Sample models."""
    name: str
    sample_type: str  #Optional[SampleType] = SampleType.food_sample
    price: Optional[float] = 0.0


class SampleDB(UUIDMixin, SampleBase, AuditMixin, table=True):
    __tablename__ = "samples"

    name: str
    sample_type: str
    price: float


class SampleRead(SampleBase):
    pass


class SampleCreate(SampleBase):
    name: str
    price: float


class SampleUpdate(SampleBase):
    sample_type: Optional[str]
