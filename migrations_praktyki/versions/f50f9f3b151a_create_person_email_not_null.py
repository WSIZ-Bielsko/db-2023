"""

create person.email not null

Revision ID: f50f9f3b151a
Creation date: 2023-07-30 11:09:48.849974

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "f50f9f3b151a"
down_revision = "eb771a06aa25"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('alter table persons alter column email set not null;')


def downgrade() -> None:
    op.execute('alter table persons alter column email drop not null;')
