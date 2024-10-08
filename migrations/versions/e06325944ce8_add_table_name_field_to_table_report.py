"""add table_name field to table report

Revision ID: e06325944ce8
Revises: 6bb29e2b7c49
Create Date: 2024-10-09 10:15:30.458711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e06325944ce8'
down_revision: Union[str, None] = '6bb29e2b7c49'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('table_report', sa.Column('table_name', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('table_report', 'table_name')
    # ### end Alembic commands ###
