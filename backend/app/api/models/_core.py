from datetime import datetime
from typing import Optional

from sqlalchemy import text
from sqlmodel import Field, SQLModel

class UUIDMixin(SQLModel):
    """Generates UUID pk for the tables.

    Usage:
        MUST GO FIRST, then the ObjectBase, then other mixins and table=true:
        `SampleStored(UUIDMixin, SampleBase, AuditMixin, table=True)`
    """
    id: Optional[int] = Field(default=None, primary_key=True)


class AuditMixin(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.now,
        nullable=False,
        sa_column_kwargs={
            "server_default": text("current_timestamp(0)")
        }
    )

    updated_at: datetime = Field(
       default_factory=datetime.now,
       nullable=True,
       sa_column_kwargs={
           "server_default": text("current_timestamp(0)"),
           "onupdate": text("current_timestamp(0)")
       }
    )
