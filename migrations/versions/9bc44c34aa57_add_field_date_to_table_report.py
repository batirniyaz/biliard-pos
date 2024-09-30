"""add field date to table report

Revision ID: 9bc44c34aa57
Revises: 90a023091d5d
Create Date: 2024-09-30 16:15:05.188878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9bc44c34aa57'
down_revision: Union[str, None] = '90a023091d5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('table_report', sa.Column('date', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('table_report', 'date')
    # ### end Alembic commands ###
