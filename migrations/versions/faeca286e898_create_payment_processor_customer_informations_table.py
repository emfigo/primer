"""create payment processor customer informations table

Revision ID: faeca286e898
Revises: ccd2988c2a17
Create Date: 2020-10-08 22:19:14.435356

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as postgresql

# revision identifiers, used by Alembic.
revision = 'faeca286e898'
down_revision = 'ccd2988c2a17'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'payment_processor_customer_informations',
        sa.Column('id', postgresql.UUID, nullable=False, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('customer_id', postgresql.UUID, sa.ForeignKey('customers.id'), nullable=False),
        sa.Column('information', postgresql.JSONB, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False, unique=True, server_default=sa.func.now()),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False, unique=True, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('payment_processor_customer_informations')
