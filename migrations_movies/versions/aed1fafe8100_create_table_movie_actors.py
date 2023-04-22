"""

create table movie_actors

Revision ID: aed1fafe8100
Creation date: 2023-04-22 12:33:01.454943

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = 'aed1fafe8100'
down_revision = '480c8a896701'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
     create table movie_actors(
        movie_id int references movies(movie_id) on DELETE cascade,
        actor_id int references actors(actor_id) on DELETE cascade,
        cast_id int,
        character text,
        credit_id text,
        gender int,
        order_ int
     );
     """)


def downgrade() -> None:
    op.execute("""
    drop table movie_actors;
    """)