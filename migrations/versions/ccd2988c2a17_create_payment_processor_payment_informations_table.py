"""create payment processor payment informations table

Revision ID: ccd2988c2a17
Revises: 5c52d32a47fb
Create Date: 2020-10-08 22:17:31.492414

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'ccd2988c2a17'
down_revision = '5c52d32a47fb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'payment_processor_payment_informations',
        sa.Column('id', postgresql.UUID, nullable=False, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('information', postgresql.JSONB, nullable=False),
        sa.Column('payment_method_id', postgresql.UUID, sa.ForeignKey('payment_methods.id'), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False, unique=True, server_default=sa.func.now()),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False, unique=True, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('payment_processor_payment_informations')
