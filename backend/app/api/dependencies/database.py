"""Database dependency injection. (Functions called as API endpoint path parameters."""
# Std Library Imports
from typing import Callable, Type

# Third-party Imports
from fastapi import Depends
from databases import Database
from starlette.requests import Request

from app.db.repositories.base import BaseRepository


def get_database(request: Request) -> Database:
    return request.app.state._db


def get_repository(Repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(db: Database = Depends(get_database)) -> Type[BaseRepository]:
        return Repo_type(db)
    
    return get_repo