from app.api.models.sample import SampleCreate, SampleDB
from app.api.services._core import CRUDMixin


class SampleCRUD(CRUDMixin):

    async def create(self, data: SampleCreate) -> SampleDB:
        values = data.model_dump()

        stored_sample = SampleDB(**values)
        self.db.add(stored_sample)
        await self.db.commit()
        await self.db.refresh(stored_sample)

        return stored_sample