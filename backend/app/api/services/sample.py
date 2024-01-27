from app.api.models.sample import SampleCreate, SampleDB
from app.api.services._core import CRUDMixin


class SampleCRUD(CRUDMixin):

    async def create(self, data: SampleCreate) -> SampleDB:
        values = data.dict()

        stored_sample = SampleDB(**values)
        self.session.add(stored_sample)
        await self.session.commit()
        await self.session.refresh(stored_sample)

        return stored_sample