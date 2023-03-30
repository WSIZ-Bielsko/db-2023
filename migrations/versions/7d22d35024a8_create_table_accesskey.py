"""

create table accesskey

Revision ID: 7d22d35024a8
Creation date: 2023-03-30 20:06:22.688568

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '7d22d35024a8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE accesskey (
        keyid SERIAL PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
        );
        """)


def downgrade() -> None:
    op.execute("""
     DROP TABLE accesskey;
     """)
