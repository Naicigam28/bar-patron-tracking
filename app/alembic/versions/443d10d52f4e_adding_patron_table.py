"""Adding Patron table

Revision ID: 443d10d52f4e
Revises: 
Create Date: 2025-02-19 13:22:46.079567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '443d10d52f4e'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    "Adds Patrons table"
    op.create_table(
        "Patrons",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("phone", sa.String, nullable=False),
        sa.Column("weight", sa.Float, nullable=False),
        sa.Column("gender", sa.String, nullable=False),
        sa.Column("birthdate", sa.Date, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime),
    )


def downgrade() -> None:
    "Removes patrons table"
    op.drop_table("Patrons")
