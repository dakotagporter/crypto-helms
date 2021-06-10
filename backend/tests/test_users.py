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

test_users_saved_password_is_hashed_and_has_salt():
    - Create a fake user by sending a POST request to the client
    - Ensure the user exists
    - Ensure the password is not the same as sent in the POST request
    - Ensure the password is hashed with the verify_password function
      from our auth service

test_can_create_access_token_successfully():
    - Ensure our auth service can properly create an access token using
      our create_access_token_for_user function from our auth service
    - Decode the token and ensure the credentials of the user and token match

test_token_missing_user_is_invalid():
    - Ensure that nothing is in the payload if a user is missing

test_invalid_token_content_raises_error():
    - Ensure that various other incorrect token contents raise the
      correct errors
"""
# Std Library Imports
from typing import List, Union, Type, Optional

# Third Party Imports
import jwt
import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from databases import Database
from pydantic import ValidationError
from starlette.datastructures import Secret

from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from app.models.user import UserCreate, UserInDB, UserPublic
from app.db.repositories.users import UsersRepository
from app.services import auth_service
from app.core.config import SECRET_KEY, JWT_ALGORITHM, JWT_AUDIENCE, JWT_TOKEN_PREFIX, ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.token import JWTMeta, JWTCreds, JWTPayload


pytestmark = pytest.mark.asyncio


class TestUserLogin:
    async def test_user_can_login_successfully_and_receives_valid_token(
        self, app: FastAPI, client: AsyncClient, test_user: UserInDB
    ) -> None:
        client.headers["content-type"] = "application/x-www-form-urlencoded"
        login_data = {
            "username": test_user.email,
            "password": "somepassword"
        }
        res = await client.post(app.url_path_for("users:login-email-and-password"), data=login_data)
        assert res.status_code == HTTP_200_OK

        token = res.json().get("access_token")
        creds = jwt.decode(token, str(SECRET_KEY), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
        assert "username" in creds
        assert creds["username"] == test_user.username
        assert sub in creds
        assert creds["sub"] == test_user.email
        assert "token_type" in res.json()
        assert res.json().get("token_type") == "bearer"
    
    @pytest.mark.parametrize(
        "credential, wrong_value, status_code"
        (
            ("email", "wrong@email.com", 401),
            ("email", None, 401),
            ("email", "notanemail", 401),
            ("password", "wrongpassword", 401)
            ("password", None, 401)
        )
    )
    async def test_user_with_wrong_creds_doesnt_receive_token(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_user: UserInDB,
        credential: str,
        wrong_value: str,
        status_code: int
    ) -> None:
        client.headers["content-type"] = "application/x-www-from-urlencoded"
        user_data = test_user.dict()
        user_data["password"] = "somepassword"
        user_data[credential] = wrong_value
        login_data = {
            "username": user_data["email"],
            "password": user_data["password"]
        }
        res = await client.post(app.url_path_for("users:login-email-and-password"), data=login_data)
        assert res.status_code == status_code
        assert "access_token" not in res.json()

class TestAuthTokens:
    async def test_can_create_access_token_successfully(
        self, app: FastAPI, client: AsyncClient, test_user: UserInDB
    ) -> None:
        access_token = auth_service.create_access_token_for_user(
            user=test_user,
            secret_key=str(SECRET_KEY),
            audience=JWT_AUDIENCE,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        creds = jwt.decode(access_token, str(SECRET_KEY), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
        assert creds.get("username") is not None
        assert creds["username"] == test_user.username
        assert creds["aud"] == JWT_AUDIENCE
    
    async def test_token_missing_user_is_invalid(self, app: FastAPI, client: AsyncClient) -> None:
        access_token = auth_service.create_access_token_for_user(
            user=None,
            secret_key=str(SECRET_KEY),
            audience=JWT_AUDIENCE,
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES
        )

        with pytest.raises(jwt.PyJWTError):
            jwt.decode(access_token, str(SECRET_KEY), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])
    
    @pytest.mark.parametrize(
        "secret_key, jwt_audience, exception"
        (
            ("wrong-secret", JWT_AUDIENCE, jwt.InvalidSignatureError),
            (None, JWT_AUDIENCE, jwt.InvalidSignatureError),
            (SECRET_KEY, "notcryptohelms:auth", jwt.InvalidAudienceError),
            (SECRET_KEY, None, jwt.InvalidAudienceError)
        )
    )
    async def test_invalid_token_content_raises_error(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_user: UserInDB,
        secret_key: Union[str, Secret],
        jwt_audience: str,
        exception: Type[BaseException]
    ) -> None:
        with pytest.raises(exception):
            access_token = auth_service.create_access_token_for_user(
                user=test_user,
                secret_key=str(secret_key),
                audience=jwt_audience,
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES
            )

            jwt.decode(access_token, str(SECRET_KEY), audience=JWT_AUDIENCE, algorithms=[JWT_ALGORITHM])


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
        created_user = UserPublic(**res.json()).dict(exclude={"access_token"})
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

        # Send post request to client to ensure success
        res = await client.post(app.url_path_for("users:register-new-user"), json={"new_user": new_user})
        assert res.status_code = status_code
    

    async def test_users_saved_password_is_hashed_and_has_salt(
        self,
        app: FastAPI,
        client: AsyncClient,
        db: Database
    ) -> None:
        user_repo = UsersRepository(db)
        new_user = {"email": "iamyou@surprise.io", "username": "heythere", "password": "supgirl"}

        # Send post request to client to ensure success
        res = await client.post(app.url_path_for("users:register-new-user"), json={"new_user": new_user})
        assert res.status_code == HTTP_201_CREATED

        # Ensure the password is hashed in the db and that
        # it's verifiable with out auth service
        user_in_db = await user_repo.get_user_by_email(email=new_user["email"])
        assert user_in_db is not None
        assert user_in_db.salt is not None and user_in_db.salt != "123"
        assert user_in_db.password != new_user["password"]
        assert auth_service.verify_password(
            password=new_user["password"],
            salt=user_in_db.salt,
            hashed_pw=user_in_db.password
        )