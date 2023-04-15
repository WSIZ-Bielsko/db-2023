"""

dodanie tabeli movies

Revision ID: e326cbf3e3e1
Creation date: 2023-04-15 13:21:46.678595

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'e326cbf3e3e1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE movies(
    movie_id int NOT NULL unique PRIMARY KEY,
    title TEXT NOT NULL
    );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS movies CASCADE;
    """)