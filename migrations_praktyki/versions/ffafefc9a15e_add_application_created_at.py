"""

add application.created_at

Revision ID: ffafefc9a15e
Creation date: 2023-08-21 10:01:29.718066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ffafefc9a15e"
down_revision = "0e841de7ac41"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('alter table applications add column created_at timestamp default now();')


def downgrade() -> None:
    op.execute('alter table applications drop column created_at')
