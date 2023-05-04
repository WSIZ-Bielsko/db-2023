"""

create table movie_crew

Revision ID: 501076e49ae0
Creation date: 2023-04-27 16:49:45.093495

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = '501076e49ae0'
down_revision = 'd4211e467915'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE movie_crew(
        credit_id TEXT,
        movie_id INT,
        person_id INT,
        job TEXT,
        department TEXT,
        gender INT,
        CONSTRAINT fk_movie_id FOREIGN KEY (movie_id)
            REFERENCES movies(movie_id),
        CONSTRAINT fk_person_id FOREIGN KEY (person_id)
            REFERENCES crew(person_id)      
    );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS movie_crew CASCADE;
    """)
