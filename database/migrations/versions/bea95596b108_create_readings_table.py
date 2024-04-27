"""create_readings_table

Revision ID: bea95596b108
Revises: ea03777c1d9f
Create Date: 2024-04-15 20:21:06.194630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bea95596b108'
down_revision = 'ea03777c1d9f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "dev_agnes_readings",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer),
        sa.Column("device_id", sa.Integer),
        sa.Column("unit", sa.String(50)),
        sa.Column("value", sa.String(50)),
        sa.Column("created_at", sa.DateTime, default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime, default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("dev_agnes_readings")
