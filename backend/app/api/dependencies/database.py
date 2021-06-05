"""Every repository needs access to the database (same with all our API
routes). Since they act as an abstraction layer for database operations,
it is required for them to always be connected to the database. With FastAPI,
'dependency injection' can be used to make our database a resource that the
application depends on to run and operate. ELI5: dependencies are just functions.
The Depends module will run the call the function provided 

get_database():
    - Uses starlette's Request module to retrieve the databases connection we
      declared earlier in the app's state object.

get_repository():
    - Takes the BaseRepository class (that only contains an empty variable
      called db) as an argument by using the Type type
    - The db variable in BaseRepository is set to the db connnection
      retrieved from get_database()
"""
# Std Library Imports
from typing import Callable, Type

# Third-party Imports
from fastapi import Depends
from databases import Database
from starlette.requests import Request

from app.db.repositories.base import BaseRepository

# Retrieve database connection
def get_database(request: Request) -> Database:
    return request.app.state._db

# Retrieve repository
def get_repository(Repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(db: Database = Depends(get_database)) -> Type[BaseRepository]:
        return Repo_type(db)
    
    return get_repo
