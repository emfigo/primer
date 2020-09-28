"""create payment methods table

Revision ID: e25e57e5acb8
Revises: 0493447dcfc8
Create Date: 2020-09-27 10:55:49.402470

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e25e57e5acb8'
down_revision = '0493447dcfc8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'payment_methods',
        sa.Column('id', postgresql.UUID, nullable=False, primary_key=True),
        sa.Column('customer_id', postgresql.UUID, sa.ForeignKey('customers.id'), nullable=False),
        sa.Column('details', postgresql.JSONB, nullable=False),
        sa.Column('payment_processor_information_id', postgresql.UUID, sa.ForeignKey('payment_processor_informations.id'), nullable=False),
        sa.Column('token', sa.String(250), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False, unique=True, server_default=sa.func.now()),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False, unique=True, server_default=sa.func.now()),
    )

    op.create_index('ik_payment_methods_token', 'payment_methods', ['token'])


def downgrade():
    op.drop_index('ik_payment_methods_token', 'customers')
    op.drop_table('payment_methods')
