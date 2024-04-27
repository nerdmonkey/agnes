"""create_loactions_table

Revision ID: a216b9e4b14c
Revises: 12a70b053a1a
Create Date: 2024-04-15 20:14:40.314906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a216b9e4b14c'
down_revision = '12a70b053a1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "dev_agnes_locations",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String(50)),
        sa.Column("description", sa.Text),
        sa.Column("parent_id", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime, default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime, default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("dev_agnes_locations")
