"""

insert values from credits.csv part 2

Revision ID: 3c2cd8fd2d64
Creation date: 2023-04-19 01:07:49.413810

"""
from pandas import read_csv
from alembic import op
from dataclasses import dataclass
from uuid import UUID


@dataclass
class Crew:
    id: int
    department: UUID
    gender: int
    job: UUID
    name: str
    credit_id: str


# revision identifiers, used by Alembic.
revision = '3c2cd8fd2d64'
down_revision = '2bcd2bba1262'
branch_labels = None
depends_on = None


cr = read_csv('/home/user/Projects/db/migrations/data/tmdb_5000_credits.csv')
def fix_text(text: str) -> str: return text.replace("'", "’")


def upgrade() -> None:
    from json import loads
    ids = []
    for index, crews in enumerate(cr['crew']):
        movie_id = cr['movie_id'][index]
        for crew in loads(crews):
            c = Crew(**crew)
            if c.id not in ids:
                ids.append(c.id)
                op.execute(f"INSERT INTO movie_crew VALUES ({movie_id}, '{c.id}')")


def downgrade() -> None:
    op.execute('DELETE FROM movie_crew;')
