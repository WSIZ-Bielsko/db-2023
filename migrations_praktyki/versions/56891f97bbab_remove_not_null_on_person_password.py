"""

remove not null on person.password

Revision ID: 56891f97bbab
Creation date: 2023-08-08 16:06:58.312029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "56891f97bbab"
down_revision = "e3031b716ab5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('alter table persons alter column password drop not null')


def downgrade() -> None:
    op.execute('alter table persons alter column password set not null')
