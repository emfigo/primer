"""create payment methods table

Revision ID: 5c52d32a47fb
Revises: f833f0e63ebe
Create Date: 2020-10-08 22:16:03.146393

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '5c52d32a47fb'
down_revision = 'f833f0e63ebe'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'payment_methods',
        sa.Column('id', postgresql.UUID, nullable=False, primary_key=True),
        sa.Column('customer_id', postgresql.UUID, sa.ForeignKey('customers.id'), nullable=False),
        sa.Column('details', postgresql.JSONB, nullable=False),
        sa.Column('token', sa.String(250), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False, unique=True, server_default=sa.func.now()),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False, unique=True, server_default=sa.func.now()),
    )

    op.create_index('ik_payment_methods_token', 'payment_methods', ['token'])


def downgrade():
    op.drop_index('ik_payment_methods_token', 'customers')
    op.drop_table('payment_methods')
