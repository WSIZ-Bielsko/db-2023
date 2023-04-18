"""

insert values from credits.csv part 3

Revision ID: b255657cc105
Creation date: 2023-04-19 02:30:13.541718

"""
from pandas import read_csv
from alembic import op
from dataclasses import dataclass

# revision identifiers, used by Alembic.
revision = 'b255657cc105'
down_revision = '3c2cd8fd2d64'
branch_labels = None
depends_on = None

cr = read_csv('/home/user/Projects/db/migrations/data/tmdb_5000_credits.csv')
def fix_text(text: str) -> str: return text.replace("'", "’")


@dataclass
class Cast:
    cast_id: int
    character: str
    credit_id: str
    gender: int
    id: int
    name: str
    order: int


def upgrade() -> None:
    from uuid import uuid4
    from json import loads
    ids = []
    cast_uuid = uuid4()
    op.execute(f"INSERT INTO job VALUES ('{cast_uuid}', 'Cast')")
    for index, casts in enumerate(cr['cast']):
        movie_id = cr['movie_id'][index]
        for cast in loads(casts):
            c = Cast(**cast)
            if c.id not in ids:
                ids.append(c.id)
                op.execute(f"INSERT INTO crew SELECT {c.id}, (SELECT department_id from department WHERE department_name = 'Actors'), {c.gender}, '{cast_uuid}', '{fix_text(c.name)}', '{c.credit_id}' WHERE NOT EXISTS(SELECT 1 FROM crew WHERE crew_id = {c.id})")
                op.execute(f"INSERT INTO movie_cast VALUES ('{fix_text(c.character)}', {movie_id}, {c.id}, {c.order}, {c.cast_id})")


def downgrade() -> None:
    op.execute('DELETE FROM movie_cast;')
    op.execute("DELETE FROM job WHERE job_name = 'Cast'")
