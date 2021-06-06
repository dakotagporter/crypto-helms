"""
User model that deals with all aspects of application users.

UserBase:
    - Contains shared information among all users

UserCreate:
    - Contains all attributes required to create a new user
    - Used in POST requests
    - Uses regex to verify a syntatically correct username

UserUpdate:
    - Attributes that can be updated (email and username can
      be update in our app)
    - Used in PUT requests
    - Uses regex to verify a syntatically correct username

UserPasswordUpdate:
    - Password can be updated by user, always ensuring it is a string
      between 7 and 100 characters

UserInDB:
    - Attributes present on a user in the database (password and salt)
    - Contains all the attributes from:
        - UserBase
        - DateTimeModelMixin
        - IDModelMixin

UserPublic:
    - Attributes present on public-facing resources being returned from
      GET, PUT or POST requests
    - Only contains attributes from:
        - UserBase
        - DateTimeModelMixin
        - IDModelMixin
    - Does NOT include password and salt
    - Let UserPublic hold an optional AccessToken allowing a user to
      be returned along with their access token as soon as they've registered
"""
# Std Library Imports
from typing import Optional

# Third Party Imports
from pydantic import EmailStr, constr

from app.models.core import DateTimeModelMixin, IDModelMixin, CoreModel
from app.models.token import AccessToken


class UserBase(CoreModel):
    """
    Class containing all the shared characteristics
    of any user (email, username, etc.).
    """
    email: Optional[EmailStr]
    user: Optional[str]
    email_verified: bool = False
    is_active: bool = True
    is_superuser: bool = False
    # Leave out password and salt for security


class UserCreate(CoreModel):
    email: EmailStr
    password: constr(min_length=7, max_length=100)
    username: constr(min_length=3, regex="^[a-zA-Z0-9_-]+$")


class UserUpdate(CoreModel):
    email: Optional[EmailStr]
    username: Optional[constr(min_length=3, regex="^[a-zA-Z0-9_-]+$")]


class UserPasswordUpdate(CoreModel):
    password: constr(min_length=7, max_length=100)
    salt: str


class UserInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    password: constr(min_length=7, max_length=100)
    salt: str


class UserPublic(IDModelMixin, DateTimeModelMixin, UserBase):
    access_token = Optional[AccessToken]