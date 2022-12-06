"""create phone number for user col

Revision ID: 619cccb773cc
Revises: 
Create Date: 2022-12-06 01:22:20.788078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '619cccb773cc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
