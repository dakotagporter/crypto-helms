"""
Hub for all fixtures used in the testing suite. Fixtures are created to run their functions
when a testing function requests it to be run.

apply_migrations():
    - Accesses the alembic.ini file to configure a migration environment
    - Runs the head migration, then downgrades

app():
    - Instantiates a new application

db():
    - Returns a database connection

client():
    - Creates a test client for testing requests
"""
# Std Library Imports
import os
import warnings

# Third Party Imports
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from databases import Database
import alembic
from alembic.config import Config

# Apply db migrations at beginning and end of testing session
@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    config = Config("alembic.ini")

    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")

# Create a new application for testing
@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.api.server import get_application
    return get_application()

# Grab a reference to our database
@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db

# Make sample requests to the running application
@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://testserver",
            headers={"Content-Type": "application/json"}
        ) as client:
            yield client