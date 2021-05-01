"""Used as abstraction layer to perform databases actions keeping persistence logic separate from application logic."""
from app.db.repositories.base import BaseRepository
from app.models.dummy import DummyCreate, DummyUpdate, DummyInDB

CREATE_DUMMY_QUERY = """
    INSERT INTO dummy (name, employee_id, age)
    VALUES (:name, :employee_id, :age)
    RETURNING id, name, employee_id, age;
"""


class DummyRepository(BaseRepository):
    """
    All database actions associated with Dummys occur here.
    """
    async def create_dummy(self, *, new_dummy: DummyCreate) -> DummyInDB:
        query_values = new_dummy.dict()
        dummy = await self.db.fetch_one(query=CREATE_DUMMY_QUERY, values=query_values)

        return DummyInDB(**dummy)