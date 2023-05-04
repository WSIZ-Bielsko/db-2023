"""

create table movies

Revision ID: edbc25e8f3b0
Creation date: 2023-04-24 13:10:05.361419

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = 'edbc25e8f3b0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE movies(
        movie_id SERIAL PRIMARY KEY,
        title TEXT
    );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS movies CASCADE;
    """)
