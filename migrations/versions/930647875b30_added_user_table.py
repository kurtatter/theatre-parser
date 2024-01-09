"""Added user table

Revision ID: 930647875b30
Revises: 
Create Date: 2024-01-08 19:15:54.296774

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '930647875b30'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=264), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('User')
    # ### end Alembic commands ###