# Std Library Imports

# Third-party Imports
from pydantic import BaseModel


class CoreModel(BaseModel):
    """
    Any common logic shared amongst all models stored here.
    """
    pass


class IDModelMixin(BaseModel):
    id: int