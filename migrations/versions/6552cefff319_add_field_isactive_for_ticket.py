"""Add field isActive for Ticket

Revision ID: 6552cefff319
Revises: 9f06e81b0d20
Create Date: 2024-01-09 19:26:51.603789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6552cefff319'
down_revision: Union[str, None] = '9f06e81b0d20'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Ticket', sa.Column('isActive', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Ticket', 'isActive')
    # ### end Alembic commands ###