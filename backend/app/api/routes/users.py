"""
User route handling user functionality.

register_new_user():
    - TL;DR -> FastAPI reads and validates the data in the request and
      sends it over to the UsersRepository to return the created user
      
    - By specifying UserCreate, FastAPI reads the body of the request as
      JSON and converts the types according to the Pydantic model, validates
      the data and errors if validation fails
    - user_repo calls on our repo dependency to retrieve the UsersRepository
      so that we can register a new user
    - Since we specified UserPublic as the return object, FastAPI automatically
      converts the UserInDB (returned from register_new_user) to a UserPublic object
    - The return value is also converted to the appropriate JSON response object.

"""
# Std Library Imports

# Third Party Imports
from fastapi import Depends, APIRouter, HTTPException, Path, Body
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.api.dependencies.database import get_repository
from app.models.user import UserCreate, UserPublic
from app.db.repositories.users import UsersRepository


router = APIRouter()


@router.post("/", response_model=UserPublic, name="users:register-new-user", status_code=HTTP_201_CREATED)
async def register_new_user(
    new_user: UserCreate = Body(..., embed=True),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository))
) -> UserPublic:
    created_user = await user_repo.register_new_user(new_user=new_user)

    return created_user