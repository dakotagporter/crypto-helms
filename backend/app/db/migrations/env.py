"""Run when the script.py.mako migration event is invoked."""
# Std Library Imports
import os
import sys
import pathlib
import logging
from logging.config import fileConfig

# Third-party Imports
import alembic
from sqlalchemy import engine_from_config, pool, create_engine
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