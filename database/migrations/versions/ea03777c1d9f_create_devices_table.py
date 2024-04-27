"""create_devices_table

Revision ID: ea03777c1d9f
Revises: a216b9e4b14c
Create Date: 2024-04-15 20:15:20.914653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea03777c1d9f'
down_revision = 'a216b9e4b14c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "dev_agnes_devices",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("category_id", sa.Integer),
        sa.Column("location_id", sa.Integer),
        sa.Column("name", sa.String(50)),
        sa.Column("topic", sa.String(50)),
        sa.Column("description", sa.Text),
        sa.Column("channel", sa.Integer),
        sa.Column("type", sa.Integer),
        sa.Column("visualization", sa.Integer),
        sa.Column("message_type", sa.Integer),
        sa.Column("created_at", sa.DateTime, default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime, default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("dev_agnes_devices")
