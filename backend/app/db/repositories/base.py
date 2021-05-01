"""Maintain a reference to established Database connections."""
from databases import Database


class BaseRepository:
    def __init__(self, db: Database) -> None:
        self.db = db