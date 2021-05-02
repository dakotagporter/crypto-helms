# Std Library Imports
from typing import Optional
from enum import Enum

# Third-party Imports

from app.models.core import CoreModel, IDModelMixin


class DummyType(str, Enum):
    dummy1 = "dummy1"
    dummy2 = "dummy2"
    dummy3 = "dummy3"


class DummyBase(CoreModel):
    """
    All common attributes of a Dummy type.
    """
    name: Optional[DummyType] = "dummy1"
    employee_id: Optional[int]
    age: Optional[int]

# Attributes required to create a new resource (used in POST requests)
class DummyCreate(DummyBase):
    employee_id: int

# Attributes that can be updated (used in PUT requests)
class DummyUpdate(DummyBase):
    name: Optional[DummyType]

# Attributes present on any resource coming out of the database
class DummyInDB(IDModelMixin, DummyBase):
    employee_id: int
    name: DummyType

# Attributes present on public-facing resources being returned from GET, POST & PUT
class DummyPublic(IDModelMixin, DummyBase):
    pass