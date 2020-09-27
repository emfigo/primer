"""create payment processor informations table

Revision ID: 0493447dcfc8
Revises: fa933040a392
Create Date: 2020-09-27 00:02:03.346900

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0493447dcfc8'
down_revision = 'fa933040a392'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'payment_processor_informations',
        sa.Column('id', postgresql.UUID, nullable=False, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('information', postgresql.JSONB, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False, unique=True, server_default=sa.func.now()),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False, unique=True, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('payment_processor_informations')
