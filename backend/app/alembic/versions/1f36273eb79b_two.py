"""two

Revision ID: 1f36273eb79b
Revises: f7ee03a62387
Create Date: 2024-11-14 15:39:37.457318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f36273eb79b'
down_revision: Union[str, None] = 'f7ee03a62387'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
