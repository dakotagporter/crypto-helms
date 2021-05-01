"""create_main_tables
Revision ID: 7410eb7efa12
Revises: 
Create Date: 2021-05-01 00:45:46.623377
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.expression import text


# revision identifiers, used by Alembic
revision = '7410eb7efa12'
down_revision = None
branch_labels = None
depends_on = None


def create_dummy_table() -> None:
    op.create_table(
        "dummy",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),  # Allows lookups by name execute faster
        sa.Column("employee_id", sa.Integer, nullable=False),
        sa.Column("age", sa.Integer, nullable=False, server_default=text('22'))
    )

def upgrade() -> None:
    create_dummy_table()

    
def downgrade() -> None:
    op.drop_table("dummy")