"""

dodanie tabeli movie_crew

Revision ID: 1c0fed7ccc14
Creation date: 2023-05-12 17:31:59.304934

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '1c0fed7ccc14'
down_revision = '7709e579a6fa'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
    create table movie_crew(
       credit_id text primary key,
       movie_id int references movies(movie_id) on delete cascade,
       crew_id int references crew(crew_id) on delete cascade,
    )
    """)

def downgrade() -> None:
    op.execute("""
    drop table movie_crew;
    """)