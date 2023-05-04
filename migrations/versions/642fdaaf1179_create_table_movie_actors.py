"""

create table movie_actors

Revision ID: 642fdaaf1179
Creation date: 2023-04-24 13:22:32.030604

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '642fdaaf1179'
down_revision = '38a2e9902da7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
CREATE TABLE movie_actors(
        credit_id   TEXT, 
        movie_id    INT,
        actor_id    INT, 
        cast_id     INT,
        character   TEXT, 
        gender      INT, 
        orders      INT,        
        CONSTRAINT fk_movie_id FOREIGN KEY (movie_id)
            REFERENCES movies(movie_id),
        CONSTRAINT fk_actor_id FOREIGN KEY (actor_id)
            REFERENCES actors(actor_id)            
    );
    """)


def downgrade() -> None:
    op.execute("""
   DROP TABLE IF EXISTS movie_actors CASCADE;
    """)
