"""
Users repository dealing with database actions on users. It inherits the
database connection from BaseRepository. Ensure that anytime the class is
called, the constructor gives the parent class the database connection.

get_user_by_email(), get_user_by_username():
    - Takes an object (provided as a kwarg) and attempts to retrieve the user
      (and all it's attributes) from the database.
    - If a user is found, all of their attributes are unpacked as keyword
      arguments and are used to create a UserInDB object.

register_new_user():
    - A UserCreate object MUST be passed
    - Ensure credentials are not already taken or existant
    - Generate a salt and hash of the users password
    - Update the param for the user by copying to a new user
    - Run the query to create a new user by unpacking all of the UserCreate's
      attributes as the values to be inserted with the SQL query
    - Return the UserInDB object

authenticate_user():
    - Checks that user is in database
    - Verify the users password with our auth service
    - python-multipart used to retrieve the password from
      the OAuth form
"""
# Std Library Imports

# Third Party Imports
from pydantic import EmailStr
from databases import Database
from fastapi import HTTPException, status

from app.db.repositories.base import BaseRepository
from app.services import auth_service
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
    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self.auth_service = auth_service

    async def authenticate_user(self, *, email: EmailStr, password: str) -> Optional[UserInDB]:
        # Check that user is in db
        user = await self.get_user_by_email(email=email)
        if not user:
            return None
        # Verify user password
        if not self.auth_service.verify_password(password=password, salt=user.salt, hashed_pw=user.password):
            return None
        
        return user
        
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
        
        user_password_update = self.auth_service.create_salt_and_hashed_password(plaintext_password=new_user.password)
        new_user_params = new_user.copy(update=user_password_update.dict())
        created_user = await self.db.fetch_one(query=REGISTER_NEW_USER, values={new_user_params.dict()})

        return UserInDB(**created_user)