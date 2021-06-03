# Std Library Imports

# Third Party Imports

from app.db.repositories.base import BaseRepository
from app.models.users import UserCreate, UserUpdate, UserInDB


class UsersRepository(BaseRepository):
    async def register_new_user(self, *, new_user: UserCreate) -> UserInDB:
        return None