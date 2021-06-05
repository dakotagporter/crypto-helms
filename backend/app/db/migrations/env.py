"""Source file run when a migration event (from the CLI) is invoked.

Alembic is used to run migrations. It's used here because it's lightweight and
works well with SQLAlchemy (which we use to communicate with out database) and
happens to be written by the same author.

Migrations are ways to change the schema of a database (add a column or table or
make updates to current schema). They're usually written as SQL transactions
(all changes run at once to ensure either a SUCCESS or FAILURE) and can therefore
be rolled back in case the changes were not correct.

The alembic environment is first configured from the alembic.ini file and the
script.py.mako will be used as a template for single migrations.

run_migrations_online():
    - Invoked when migration is run from CLI
    - Connects to either current or testing database and will run current migrations
    - TESTING: Creates a fresh testing database from the URL we know to be valid

run_migrations_offline():
    - Will run ONLY testing migrations while offline

RUNNING MIGRATIONS:
> docker ps
> docker exec -it <server_container_id> bash
> alembic revision -m "<migration_description>"

    - Define any additional functions (or add code to upgrade() and downgrade())
      in the new file generated in app.db.migrations.versions

> alembic upgrade head

    - Use the pgadmin docker service (port 80) to ensure that migrations
      were successful
"""
# Std Library Imports
import os
import sys
import pathlib
import logging
from logging.config import fileConfig

# Third Party Imports
import alembic
from sqlalchemy import create_engine
from psycopg2 import DatabaseError

# Append app directory to current path to easily import config
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.core.config import DATABASE_URL, RDS_DB_NAME

# Instantiate alembic config object to pull values from .ini file
config = alembic.context.config

# Parse config file
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    """
    DB_URL = f"{DATABASE_URL}_test" if os.environ.get("TESTING") else str(DATABASE_URL)
    
    # Handle testing configurations for migrations
    if os.environ.get("TESTING"):
        # Connect to primary database
        default_engine = create_engine(str(DATABASE_URL), isolation_level="AUTOCOMMIT")
        # Drop testing db if exists and create fresh db
        with default_engine.connect() as default_conn:
            default_conn.execute(f"DROP DATABASE IF EXISTS {RDS_DB_NAME}_test")
            default_conn.execute(f"CREATE DATABASE {RDS_DB_NAME}_test")

    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", str(DB_URL))

    if connectable is None:
        logger.warn("--- CREATING CONNECTION ---")
        connectable = create_engine(
            f"postgres://{RDS_USER}:{RDS_PASSWORD}@{DATABASE_URL}:{RDS_PORT}"
        )
    
    with connectable.connect() as connection:
        alembic.context.configure(
            connection=connection,
            target_metadata=None
        )

        with alembic.context.begin_transaction():
            logger.info("--- RUNNING MIGRATIONS ---")
            alembic.context.run_migrations()
            logger.info("--- MIGRATIONS COMPLETE ---")


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    """
    if os.environ.get("TESTING"):
        raise DatabaseError("Running testing migrations offline currently not permitted.")

    alembic.context.configure(url=str(DATABASE_URL))

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


if alembic.context.is_offline_mode():
    logger.info("Running migrations offline ..")
    run_migrations_offline()
else:
    logger.info("Running migrations online ..")
    run_migrations_online()