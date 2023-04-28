"""

create table movie_crew

Revision ID: e9cebc549ba3
Creation date: 2023-04-25 20:26:39.196303

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'e9cebc549ba3'
down_revision = '49515c3e0691'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
    CREATE TABLE movie_crew(
    movie_id int references movies(movie_id) on delete cascade,
    genre_id int references crew(crew_id) on delete cascade
    );
    """)

def downgrade() -> None:
    op.execute(
        f"""--sql
        drop table if exists movie_crew cascade
        """)
