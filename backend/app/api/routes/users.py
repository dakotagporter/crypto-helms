"""
User route handling user functionality.

register_new_user():
    - TL;DR -> FastAPI reads and validates the data in the request and
      sends it over to the UsersRepository to return the created user
      along with their access token
      
    - By specifying UserCreate, FastAPI reads the body of the request as
      JSON and converts the types according to the Pydantic model, validates
      the data and errors if validation fails
    - user_repo calls on our repo dependency to retrieve the UsersRepository
      so that we can register a new user
    - Since we specified UserPublic as the return object, FastAPI automatically
      converts the UserInDB (returned from register_new_user) to a UserPublic object
    - The return value is also converted to the appropriate JSON response object.

user_login_with_email_and_password():
    - Calls on our authenticate_user function from the user repository to ensure
      that the user is correct
    - An access token is then created for the user and sent back to the owner
"""
# Std Library Imports

# Third Party Imports
from fastapi import Depends, APIRouter, HTTPException, Path, Body
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import (
  HTTP_200_OK,
  HTTP_201_CREATED,
  HTTP_400_BAD_REQUEST,
  HTTP_401_UNAUTHORIZED,
  HTTP_404_NOT_FOUND,
  HTTP_422_UNPROCESSABLE_ENTITY
)

from app.api.dependencies.database import get_repository
from app.models.user import UserCreate, UserPublic
from app.db.repositories.users import UsersRepository
from app.models.token import AccessToken
from app.services import auth_service


router = APIRouter()


@router.post("/login/token/", response_model=AccessToken, name="users:login-email-and-password")
async def user_login_with_email_and_password(
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm) 
) -> AccessToken:
    user = await user_repo.authenticate_user(email=form_data.username, password=form_data.password)

    if not user:
      raise HTTPException(
          status_code=HTTP_401_UNAUTHORIZED,
          detail="Authentication was unsuccessful.",
          headers={"WWW-Authenticate": "Bearer"}
      )
    
    access_token = AccessToken(access_token=auth_service.create_access_token_for_user(user=user), token_type="bearer")

    return access_token

@router.post("/", response_model=UserPublic, name="users:register-new-user", status_code=HTTP_201_CREATED)
async def register_new_user(
    new_user: UserCreate = Body(..., embed=True),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository))
) -> UserPublic:
    created_user = await user_repo.register_new_user(new_user=new_user)

    access_token = AccessToken(
      access_token=auth_service.create_access_token_for_user(user=created_user), token_type="bearer"
    )

    return UserPublic(**created_user.dict(), access_token=access_token)