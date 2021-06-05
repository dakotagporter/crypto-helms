"""
Testing of user route.

test_routes_exist():
    - Creates a fake new user
    - Waits for a response when pinging the register-new-user route

test_users_can_register_successfully():
    - Sets a new database connection when accessing the users repository
    - Creates a fake new user
    - Query database to ensure user does not exist
    - Send POST request to register new user
    - Query for user again to ensure successful creation

test_user_registration_fails_when_credentials_are_taken():
    - Parametrize decorator allows test function to be called multiple
      times (to test all bad error codes) by writing over the default
      values provided in the fake new user
"""
# Std Library Imports

# Third Party Imports
import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from databases import Database

from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from app.models.user import UserCreate, UserInDB
from app.db.repositories.users import UsersRepository


pytestmark = pytest.mark.asyncio


class TestUserRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        new_user = {"email": "test@email.io", "username": "test_username", "password": "testpassword"}
        res = await client.post(app.url_path_for("users:register-new-user"), json={"new_user": new_user})
        assert res.status_code != HTTP_404_NOT_FOUND


class TestUserRegistration:
    async def test_users_can_register_successfully(
        self,
        app: FastAPI,
        client: AsyncClient,
        db: Database
    ) -> None:
        user_repo = UsersRepository(db)
        new_user = {"email": "crsr@gmail.com", "username": "CRSR", "password": "pass-word"}

        # Ensure that user does NOT yet exist
        user_in_db = await user_repo.get_user_by_email(email=new_user["email"])
        assert user_in_db is None

        # Send POST request to create a new user and ensure status
        res = await client.post(app.url_path_for("user:register-new-user"), json={"new_user": new_user})
        assert res.status_code == HTTP_201_CREATED

        # Ensure that new user exists in db
        user_in_db = await user_repo.get_user_by_email(email=new_user["email"])
        assert user_in_db is not None
        assert user_in_db.email = new_user["email"]
        assert user_in_db.username = new_user["username"]

        # Check that user returned in response is the same as the one in the db
        created_user = UserInDB(**res.json(), password="whatever", salt="1234").dict(exclude={"password", "salt"})
        assert created_user == user_in_db.dict(exclude={"password", "salt"})
    
    @pytest.mark.parametrize(
        "attr, value, status_code",
        (
            ("email", "crsr@gmail.com", 400),
            ("username", "CRSR", 400),
            ("email", "invalid@email@email.com", 422),
            ("password", "short", 422),
            ("username", "crsr47@$$xx", 422),
            ("username", "ab", 422)
        )
    )
    async def test_user_registration_fails_when_credentials_are_taken(
        self,
        app: FastAPI,
        client: AsyncClient,
        db: Database,
        attr: str,
        value: str,
        status_code: int
    ) -> None:
        new_user = {"email": "nottaken@gmail.com", "username": "username_not_taken", "password": "anypassword"}
        new_user[attr] = value

        res = await client.post(app.url_path_for("users:register-new-user"), json={"new_user": new_user})
        assert res.status_code = status_code