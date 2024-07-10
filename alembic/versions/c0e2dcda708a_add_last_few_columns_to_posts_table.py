"""add last few columns to posts table

Revision ID: c0e2dcda708a
Revises: 733b1839a8bf
Create Date: 2024-07-09 21:28:21.379595

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0e2dcda708a'
down_revision: Union[str, None] = '733b1839a8bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa. TIMESTAMP(timezone=True), nullable=False, server_default=sa.text
        ('NOW()')),)
    pass


def downgrade() :
    op.drop_column('post','published')
    op.drop_column('post','created_at')
    pass
