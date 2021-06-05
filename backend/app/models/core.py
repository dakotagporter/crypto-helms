"""
Pydantic uses the same idea as dataclasses (classes that focus more on storing
state rather than logic) to deal with data validation (for speed and security)
to ensure that data flowing throughout the application is what it's supposed to be.

The typing library allows us to use Python type hints to help with the data
validation process within FastAPI and Pydantic.
    - Optional[...]: The argument MUST be ... or None.
    - List[...], Tuple[...], etc.

CoreModel:
    - All new models we create will inherit from CoreModel, because we can
      add functionality to Pydantic's BaseModel so that all of our new
      models can have shared logic that we define.

DateTimeModelMixin:
    - Takes an optionally provided datetime object and uses a custom validator decorator
      (only allowed to be used on a class method) to ensure that the created_at
      (then updated_at subsequently) variable is a datetime object. If it is, return back
      the value and, if not, return a new, current datetime object.

IDModelMixin:
    - This class is used for any resource coming from the database
    - No default argument is provided to id, so an id MUST be
      provided for any new instances
"""
# Std Library Imports
from typing import Optional
from datetime import datetime

# Third Party Imports
from pydantic import BaseModel, validator


class CoreModel(BaseModel):
    """
    Any common logic shared amongst all models stored here.
    """
    pass


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.datetime.now()


class IDModelMixin(BaseModel):
    id: int