# DB related HOW-TOs

## Migrations
See makefile commands staring with `mig-``.

## Cookbook & Troubleshooting
### Declare enums
1. Declare the main table normally, as SQLModel table. 
2. Declare the enum model inheriting from `enum.Enum` (and **NOT** `SQLModel enum`).
3. Link enum to the table typing the linked fieldname with the enum class name.

Here is an example:

```python
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel

from app.api.models._core import UUIDMixin, AuditMixin


class SampleType(str, Enum):
   food_sample = "food"
   paint_sample = "paint"


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
```
4. Then after running migrations autogenerate command, you'll have a table with an enum field, like this:

    ```python
    sa.Column('sample_type', 
        sa.Enum('food_sample', 'paint_sample', name='sampletype'),
    nullable=False),
   ```
5. To ensure migration down deletes the enum properly, after dropping the table, drop the enum by its name (no underscore) like this:

    ```python
    op.drop_table('samples')
    sa.Enum('food_sample', 'paint_sample', name='sampletype').drop(op.get_bind())
   ```
You can check the result in your DB manager, under `db > schemas > public > data types`: `sampletype` and `_sampletype` should not be there anymore.