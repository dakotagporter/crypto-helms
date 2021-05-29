"""create_main_tables
Revision ID: 7410eb7efa12
Revises: 
Create Date: 2021-05-01 00:45:46.623377
"""

from typing import Tuple
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '7410eb7efa12'
down_revision = None
branch_labels = None
depends_on = None


def create_updated_at_trigger() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )


def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed
        )
    )


def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("email", sa.Text, unique=True, nullable=False, index=True),
        sa.Column("email_verified", sa.Text, sa.Boolean, nullable=False, server_default=False),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("password", sa.Text, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=True),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default=False),
        *timestamps()
    )
    op.execute(
        """
        CREATE TRIGGER update_user_modtime
            BEFORE UPDATE
            ON users
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_dummy_table() -> None:
    op.create_table(
        "dummy",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),  # Allows lookups by name execute faster
        sa.Column("employee_id", sa.Integer, nullable=False),
        sa.Column("age", sa.Integer, nullable=False, server_default=text('22'))
    )


def upgrade() -> None:
    create_updated_at_trigger()
    create_users_table()
    create_dummy_table()

    
def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("dummy")
    op.execute("DROP FUNCTION update_updated_at_column")