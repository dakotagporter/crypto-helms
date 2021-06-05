"""
Users repository dealing with database actions on users. It inherits the
database connection from BaseRepository.

get_user_by_email(), get_user_by_username():
    - Takes an object (provided as a kwarg) and attempts to retrieve the user
      (and all it's attributes) from the database.
    - If a user is found, all of their attributes are unpacked as keyword
      arguments and are used to create a UserInDB object.

register_new_user():
    - A UserCreate object MUST be passed
    - Ensure credentials are not already taken or existant
    - Run the query to create a new user by unpacking all of the UserCreate's
      attributes as the values to be inserted with the SQL query
    - Return the UserInDB object
"""
# Std Library Imports

# Third Party Imports
from pydantic import EmailStr
from fastapi import HTTPException, status

from app.db.repositories.base import BaseRepository
from app.models.user import UserCreate, UserUpdate, UserInDB, UserPublic


GET_USER_BY_EMAIL = """
    SELECT id, username, email, email_verified, password, salt, is_active, is_superuser, created_at, updated_at
    FROM users
    WHERE email = :email;
"""

GET_USER_BY_USERNAME = """
    SELECT id, username, email, email_verified, password, salt, is_active, is_superuser, created_at, updated_at
    FROM users
    WHERE username = :username;
"""

REGISTER_NEW_USER = """
    INSERT INTO users (username, email, password, salt)
    VALUES (:username, :email, :password, :salt)
    RETURNING id, username, email, email_verified, password, salt, is_active, is_superuser, created_at, updated_at;
"""


class UsersRepository(BaseRepository):
    async def get_user_by_email(self, *, email: EmailStr) -> UserInDB:
        user_record = await self.db.fetch_one(query=GET_USER_BY_EMAIL, values={"email": email})

        if not user_record:
            return None

        return UserInDB(**user_record)
    
    async def get_user_by_username(self, *, username: str) -> UserInDB:
        user_record = await self.db.fetch_one(query=GET_USER_BY_USERNAME, values={"username": username})

        if not user_record:
            return None

        return UserInDB(**user_record)

    async def register_new_user(self, *, new_user: UserCreate) -> UserInDB:
        # Ensure email is not already taken
        if await self.get_user_by_email(email=new_user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists in database. Login with that email or register with different one."
            )
        
        # Ensure username is not already taken
        if await self.get_user_by_username(username=new_user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is already taken. Please try a different one."
            )
        
        created_user = await self.db.fetch_one(query=REGISTER_NEW_USER, values={**new_user.dict(), "salt": "123"})

        return UserInDB(**created_user)