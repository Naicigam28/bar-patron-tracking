"""Track Patron Drinks

Revision ID: 120d8b1a4dca
Revises: 443d10d52f4e
Create Date: 2025-02-22 15:42:21.965133

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "120d8b1a4dca"
down_revision: Union[str, None] = "443d10d52f4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Adding table to keep track of patron drinks"""
    op.create_table(
        "PatronDrinks",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("patron_id", sa.Integer, sa.ForeignKey("Patrons.id"), nullable=False),
        sa.Column("drink_id", sa.Integer, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
        sa.Column("deleted_at", sa.DateTime),
        sa.Column("alcohol_type", sa.String, nullable=False),
        sa.Column("volume", sa.Float, nullable=False),
        sa.Column("abv", sa.Float, nullable=False),
    )


def downgrade() -> None:
    """Dropping table to keep track of patron drinks"""
    op.drop_table("PatronDrinks")
