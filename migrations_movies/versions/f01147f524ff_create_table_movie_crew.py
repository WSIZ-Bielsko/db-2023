"""

create table movie_crew

Revision ID: f01147f524ff
Creation date: 2023-05-02 22:03:48.650747

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'f01147f524ff'
down_revision = 'ca4621e08ef9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE movie_crew(
    movie_id int references movies(movie_id) on DELETE CASCADE,
    crew_id int,
    name text,
    gender int,
    credit_id text,
    department text,
    job text,
    CONSTRAINT fk_crew FOREIGN KEY (crew_id, name, gender) 
    REFERENCES crew(crew_id, name, gender) ON DELETE CASCADE
    );
    """)

def downgrade() -> None:
    op.execute(
        f"""--sql
        drop table if exists movie_crew cascade
        """)