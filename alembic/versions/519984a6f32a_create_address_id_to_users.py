"""create address_id to users

Revision ID: 519984a6f32a
Revises: c3e753aa249b
Create Date: 2022-12-06 01:39:34.775898

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '519984a6f32a'
down_revision = 'c3e753aa249b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('address_users_fk', source_table='users', referent_table='address',
                          local_cols=['address_id'], remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('address_users_fk', table_name='users')
    op.drop_column('users', 'address_id')
