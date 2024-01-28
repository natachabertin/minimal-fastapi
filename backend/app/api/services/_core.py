from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDMixin:
    """Parent of all basic CRUD operations, allows database interaction."""
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
