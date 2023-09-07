"""

ALTER TABLE persons ADD active bool DEFAULT True;

Revision ID: a1a75aaa309c
Creation date: 2023-07-20 15:26:40.695711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a1a75aaa309c"
down_revision = "67d359af9480"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE persons
        ADD active bool
        DEFAULT True;
        """
    )


def downgrade() -> None:
    op.execute(
        """
        ALTER TABLE persons
        DROP COLUMN active;
        """
    )
