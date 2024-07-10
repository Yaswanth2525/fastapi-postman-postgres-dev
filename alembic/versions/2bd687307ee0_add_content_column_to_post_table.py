"""add content column to post table

Revision ID: 2bd687307ee0
Revises: 44ee2af27501
Create Date: 2024-07-09 12:19:45.461259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2bd687307ee0'
down_revision: Union[str, None] = '44ee2af27501'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('post',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('post','content')
    pass
