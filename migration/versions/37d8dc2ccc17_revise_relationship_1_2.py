"""revise relationship 1.2

Revision ID: 37d8dc2ccc17
Revises: 71e7bc106c70
Create Date: 2023-08-26 18:26:04.200638

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37d8dc2ccc17'
down_revision: Union[str, None] = '71e7bc106c70'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
