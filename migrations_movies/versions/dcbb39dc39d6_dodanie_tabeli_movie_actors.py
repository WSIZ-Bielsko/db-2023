"""

dodanie tabeli movie_actors

Revision ID: dcbb39dc39d6
Creation date: 2023-04-15 13:31:54.874559

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'dcbb39dc39d6'
down_revision = '8dce3beada60'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE movie_actors(
    cast_id int NOT NULL unique PRIMARY KEY,
    movie_id int references movies(movie_id) on delete cascade,
    actor_id int references actors(actor_id) on delete cascade,
    credit_id TEXT,
    character TEXT,
    gender int,
    position int
    );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS movie_actors CASCADE;
    """)