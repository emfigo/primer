"""create customers table

Revision ID: fa933040a392
Revises: None
Create Date: 2020-09-26 22:56:40.515212

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as postgresql


# revision identifiers, used by Alembic.
revision = 'fa933040a392'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'customers',
        sa.Column('id', postgresql.UUID, nullable=False, primary_key=True),
        sa.Column('first_name', sa.String(20), nullable=False),
        sa.Column('last_name', sa.String(20), nullable=False),
        sa.Column('company', sa.String(15), nullable=True),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('phone', sa.String(20), nullable=False),
        sa.Column('fax', sa.String(20), nullable=False),
        sa.Column('website', sa.String(250), nullable=False),
        sa.Column('token', sa.String(1000), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False, unique=True, server_default=sa.func.now()),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False, unique=True, server_default=sa.func.now()),
    )

    op.create_unique_constraint('uq_customers_email', 'customers', ['email'])
    op.create_index('ik_customers_email', 'customers', ['email'])


def downgrade():
    op.drop_index('ik_customers_email', 'customers')
    op.drop_constraint('uq_customers_email', 'customers')
    op.drop_table('customers')

