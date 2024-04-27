"""create_categories_table

Revision ID: 12a70b053a1a
Revises: be6c69c1a61a
Create Date: 2024-04-15 20:11:48.929836

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12a70b053a1a'
down_revision = 'be6c69c1a61a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "dev_agnes_categories",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String(50)),
        sa.Column("description", sa.Text),
        sa.Column("parent_id", sa.Integer, nullable=True),
        sa.Column("created_at", sa.DateTime, default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime, default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("dev_agnes_categories")
