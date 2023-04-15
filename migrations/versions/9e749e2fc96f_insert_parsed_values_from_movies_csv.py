"""

insert parsed values from movies csv

Revision ID: 9e749e2fc96f
Creation date: 2023-04-15 22:06:04.515201

"""
import pandas as pd
from alembic import op
from dataclasses import dataclass
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '9e749e2fc96f'
down_revision = 'f7f8d9d25ab9'
branch_labels = None
depends_on = None

pd.options.display.max_rows = 10
mv = pd.read_csv('/home/user/Projects/db/migrations/data/tmdb_5000_movies.csv')


@dataclass
class Generic:
    id: int
    name: str


@dataclass
class Country:
    iso_3166_1: str
    name: str


@dataclass
class Language:
    iso_639_1: str
    name: str


class Genre(Generic): pass
class Keyword(Generic): pass
class Company(Generic): pass
class Status(Generic): pass


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
    release_date: datetime
    revenue: int
    runtime: int
    status: int
    tagline: str
    vote_average: float
    vote_count: int


def fix_text(text: str) -> str: return text.replace("'", "’").replace(' :', ': ')


def parse_json_columns(column_name: str, object_class):
    from json import loads
    names = []
    for x in mv[column_name]:
        for y in loads(x):
            obj = object_class(**y)
            obj.name = fix_text(obj.name)
            if obj.name not in names:
                names.append(obj.name)
                op.execute(f'INSERT INTO {object_class.__name__.lower()} VALUES {tuple(obj.__dict__.values())}')


def import_movies():
    status_ar, int_f = ['Released', 'Post Production', 'Rumored'], ['budget', 'revenue', 'runtime']
    text = ['homepage', 'original_title', 'overview', 'tagline', 'title']
    column_args = [('production_countries', Country), ('spoken_languages', Language), ('genres', Genre), ('production_companies', Company), ('keywords', Keyword) ]
    op.execute("INSERT INTO language VALUES ('nb', 'Norwegian Bokmal')")
    for index, status in enumerate(status_ar): op.execute(f"INSERT INTO status VALUES ({index}, '{status}')")
    for args in column_args: parse_json_columns(*args)
    for i in mv.T:
        values = {prop: mv[prop][i] for prop in list(Movie.__annotations__.keys())}
        movie = Movie(**values)
        movie.status = status_ar.index(movie.status)
        for field in text:
            if isinstance(movie.__getattribute__(field), float): movie.__setattr__(field, "NULL")
            else: movie.__setattr__(field, fix_text(movie.__getattribute__(field)))
        for field in int_f:
            if isinstance(movie.__getattribute__(field), float): movie.__setattr__(field, 0)
        if isinstance(movie.release_date, float): movie.release_date = "1900-01-01"
        op.execute(f'INSERT INTO movie VALUES {tuple(movie.__dict__.values())}')


def upgrade():
    import_movies()


def downgrade() -> None:
    op.execute("""
    DELETE FROM movie;
    DELETE FROM genre;
    DELETE FROM keyword;
    DELETE FROM company;
    DELETE FROM country;
    DELETE FROM language;
    """)
