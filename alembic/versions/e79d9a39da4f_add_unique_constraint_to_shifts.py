"""Add unique constraint to shifts

Revision ID: e79d9a39da4f
Revises: 2b7baec7188b
Create Date: 2023-11-24 14:42:41.448663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e79d9a39da4f'
down_revision: Union[str, None] = '2b7baec7188b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_user_date_uc', 'shifts', ['user_id', 'date'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_user_date_uc', 'shifts', type_='unique')
    # ### end Alembic commands ###
