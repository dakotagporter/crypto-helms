"""
These repositories serve as an abstraction layer over all of our database
operations. This enables us to split database functionality from the overall
application functionality (if one fails, the whole thing won't come crashing down).

BaseRepository:
    - Maintains a connection to our database
"""
# Std Library Imports

# Third Party Imports
from databases import Database


class BaseRepository:
    def __init__(self, db: Database) -> None:
        self.db = db