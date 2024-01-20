from datetime import datetime
from typing import Optional

from sqlalchemy import text
from sqlmodel import Field, SQLModel


class DBMixin(SQLModel):
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

    deleted_at: datetime = Field(
       default_factory=datetime.now,
       nullable=True,
       sa_column_kwargs={
           "server_default": text("current_timestamp(0)"),
           "ondelete": text("current_timestamp(0)")
       }
    )
