"""create customers table

Revision ID: f833f0e63ebe
Revises: None
Create Date: 2020-10-08 22:14:53.738689

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as postgresql


# revision identifiers, used by Alembic.
revision = 'f833f0e63ebe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'customers',
        sa.Column('id', postgresql.UUID, nullable=False, primary_key=True),
        sa.Column('first_name', sa.String(20), nullable=False),
        sa.Column('last_name', sa.String(20), nullable=False),
        sa.Column('company', sa.String(50), nullable=True),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('phone', sa.String(20), nullable=False),
        sa.Column('fax', sa.String(20)),
        sa.Column('website', sa.String(250)),
        sa.Column('token', sa.String(256), nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False, unique=True, server_default=sa.func.now()),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False, unique=True, server_default=sa.func.now()),
    )

    op.create_unique_constraint('uq_customers_email', 'customers', ['email'])
    op.create_index('ik_customers_email', 'customers', ['email'])
    op.create_index('ik_customers_token', 'customers', ['token'])


def downgrade():
    op.drop_index('ik_customers_email', 'customers')
    op.drop_index('ik_customers_token', 'customers')
    op.drop_constraint('uq_customers_email', 'customers')
    op.drop_table('customers')
