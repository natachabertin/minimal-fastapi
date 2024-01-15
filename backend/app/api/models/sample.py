from sqlalchemy.dialects import postgresql
from sqlalchemy import event
from sqlmodel import SQLModel

role_type = postgresql.ENUM(
   "mage",
   "assassin",
   "warrior",
   "priest",
   "tank",
   name=f"role"
)
https://medium.com/@estretyakov/the-ultimate-async-setup-fastapi-sqlmodel-alembic-pytest-ae5cdcfed3d4

@event.listens_for(SQLModel.metadata, "before_create")
def _create_enums(metadata, conn, **kw):  # noqa: indirect usage
   hrs_role_type.create(conn, checkfirst=True)
