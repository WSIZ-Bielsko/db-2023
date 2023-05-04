"""

create table movie genres

Revision ID: a4775aa32a71
Creation date: 2023-04-29 12:54:17.123765

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = 'a4775aa32a71'
down_revision = 'e3042774f401'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE movie_genres(
    movie_id int references movies(movie_id) on delete cascade,
    genre_id int references genres(genre_id) on delete cascade
    );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS movie_genres CASCADE;
    """)
