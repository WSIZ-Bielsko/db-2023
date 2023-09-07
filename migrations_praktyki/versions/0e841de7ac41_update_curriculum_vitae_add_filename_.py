"""

update curriculum vitae add filename not null

Revision ID: 0e841de7ac41
Creation date: 2023-08-07 14:39:23.657823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0e841de7ac41"
down_revision = "56891f97bbab"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE curriculum_vitae ADD COLUMN filename TEXT NOT NULL DEFAULT ''; 
        """
    )


def downgrade() -> None:
    op.execute("""ALTER TABLE curriculum_vitae DROP COLUMN IF EXISTS filename""")
