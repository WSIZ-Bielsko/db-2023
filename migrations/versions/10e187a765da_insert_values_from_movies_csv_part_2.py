"""

insert values from movies.csv part 2

Revision ID: 10e187a765da
Creation date: 2023-04-16 11:32:00.290843

"""
from alembic import op
from dataclasses import dataclass
from datetime import date
from pandas import read_csv

status_ar = ['Released', 'Post Production', 'Rumored']
mv = read_csv('/home/user/Projects/db/migrations/data/tmdb_5000_movies.csv')

# revision identifiers, used by Alembic.
revision = '10e187a765da'
down_revision = '5e8358028b93'
branch_labels = None
depends_on = None


@dataclass
class Movie:
    id: int
    budget: int
    title: str
    homepage: str
    original_language: str
    original_title: str
    overview: str
    popularity: float
    release_date: date
    revenue: int
    runtime: int
    status: int
    tagline: str
    vote_average: float
    vote_count: int


def fix_text(text: str) -> str: return text.replace("'", "’").replace(' :', ': ')


def upgrade() -> None:
    from json import loads
    int_f, text = ['budget', 'revenue', 'runtime'], ['homepage', 'original_title', 'overview', 'tagline', 'title']
    spoken = [y['iso_639_1'] for x in mv['spoken_languages'] for y in loads(x)]
    for x in mv['original_language']:
        if x not in spoken: op.execute(f"INSERT INTO language VALUES ('{x}', '???')")
    for i in mv.T:
        values = {prop: mv[prop][i] for prop in list(Movie.__annotations__.keys())}
        movie = Movie(**values)
        movie.status = status_ar.index(movie.status)
        for field in text:
            if isinstance(movie.__getattribute__(field), float): movie.__setattr__(field, "NULL")
            else: movie.__setattr__(field, fix_text(movie.__getattribute__(field)))
        for field in int_f:
            if isinstance(movie.__getattribute__(field), float): movie.__setattr__(field, 0)
        if isinstance(movie.release_date, float): movie.release_date = "1-1-1"
        op.execute(f'INSERT INTO movie VALUES {tuple(movie.__dict__.values())}')


def downgrade() -> None:
    op.execute('DELETE FROM movie;')
