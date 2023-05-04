"""

create table languages

Revision ID: e6d1ba467e61
Creation date: 2023-04-29 12:39:33.317916

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = 'e6d1ba467e61'
down_revision = '501076e49ae0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE languages (
        lang_id VARCHAR(2) UNIQUE PRIMARY KEY,
        lang TEXT NOT NULL
    );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS languages CASCADE;
    """)
