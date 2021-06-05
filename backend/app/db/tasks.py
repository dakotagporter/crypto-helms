"""Collection of database tasks to be executed throughout application runtime.

logger:
    - Creates a logger for database status throughout application runtime
    
connect_to_db():
    - Retrieves AWS database credentials from app.core.config
    - Connects to database and attach the connection (as _db) to the app's state object (for constant connection)
    - Raise error in logger if connection fails

close_db_connection():
    - app.state._db is an established db connection and can
      be closed using databases .diconnect() method
    - Raise error in logger if disconnect fails
"""
# Std Library Imports
import os
import logging

# Third Party Imports
from databases import Database
from fastapi import FastAPI
import boto3

from app.core import config

logger = logging.getLogger(__name__)

# Connect to database using credentials from core.config
async def connect_to_db(app: FastAPI) -> None:
    # Assign testing database when called from conftest
    DB_URL = f"{config.DATABASE_URL}_test" if os.environ.get("TESTING") else config.DATABASE_URL
    database = Database(DB_URL)

    try:
        # Connect to database
        database = Database(config.DATABASE_URL)

        # Establish app database connection state
        await database.connect()
        app.state._db = database

    except Exception as e:
        logger.warn("--- DB CONNECTION ERROR ---")
        logger.warn(e)
        logger.warn("--- DB CONNECTION ERROR ---")

# Close database connection
async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        logger.warn("--- DB DISCONNECT ERROR ---")
        logger.warn(e)
        logger.warn("--- DB DISCONNECT ERROR ---")