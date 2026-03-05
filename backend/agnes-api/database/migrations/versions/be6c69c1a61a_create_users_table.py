"""create users table

Revision ID: be6c69c1a61a
Revises:
Create Date: 2023-10-19 08:14:26.664619

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "be6c69c1a61a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("username", sa.String(50), unique=True, index=True),
        sa.Column("email", sa.String(50), unique=True, index=True),
        sa.Column("password", sa.String(100)),
        sa.Column("created_at", sa.DateTime, default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime, default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
