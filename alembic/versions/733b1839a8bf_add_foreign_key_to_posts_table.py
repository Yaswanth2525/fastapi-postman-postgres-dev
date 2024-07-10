"""add foreign-key to posts table

Revision ID: 733b1839a8bf
Revises: 8699134b70f8
Create Date: 2024-07-09 20:30:19.088057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '733b1839a8bf'
down_revision: Union[str, None] = '8699134b70f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.add_column('post',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table='post',referent_table='users',local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk',table_name='post')
    op.drop_column('post','owner_id')
    pass
