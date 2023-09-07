"""

update persons add password, unique email

Revision ID: f823ee4f375a
Creation date: 2023-07-28 15:22:37.184798

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f823ee4f375a"
down_revision = "e36ae7df8803"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE persons add COLUMN password TEXT NOT NULL default '';
    ALTER TABLE persons ADD CONSTRAINT uq_email UNIQUE (email);
    """)


def downgrade() -> None:
    op.execute("""alter table persons drop column if exists password """)
    op.execute("""alter table persons drop constraint uq_email""")
