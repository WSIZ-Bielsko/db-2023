"""

dodanie tabeli movie_genres

Revision ID: b355e311da60
Creation date: 2023-04-22 13:10:37.069586

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'b355e311da60'
down_revision = '2e4052030729'
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