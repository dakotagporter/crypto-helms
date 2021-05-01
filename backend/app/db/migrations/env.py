"""Run when the script.py.mako migration event is invoked."""
# Std Library Imports
import sys
import pathlib
import logging
from logging.config import fileConfig

# Third-party Imports
import alembic
from sqlalchemy import engine_from_config, pool, create_engine

# Append app directory to current path to easily import config
sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

from app.core import config as cfg

# Instantiate alembic config object to pull values from .ini file
config = alembic.context.config

# Parse config file
fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    """
    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", str(cfg.RFC1738_DATABASE_URL))

    if connectable is None:
        logger.warn("--- CREATING CONNECTION ---")
        connectable = create_engine(
            f"postgres://{cfg.RDS_USER}:{cfg.RDS_PASSWORD}@{cfg.DATABASE_URL}:{cfg.RDS_PORT}"
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
    alembic.context.configure(url=str(cfg.RFC1738_DATABASE_URL))

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


if alembic.context.is_offline_mode():
    logger.info("Running migrations offline ..")
    run_migrations_offline()
else:
    logger.info("Running migrations online ..")
    run_migrations_online()