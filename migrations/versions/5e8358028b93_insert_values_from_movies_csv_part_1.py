"""

insert values from movies.csv part 1

Revision ID: 5e8358028b93
Creation date: 2023-04-16 11:26:00.126371

"""
from pandas import read_csv
from alembic import op
from dataclasses import dataclass
from json import loads

status_ar = ['Released', 'Post Production', 'Rumored']
mv = read_csv('/home/user/Projects/db/migrations/data/tmdb_5000_movies.csv')


# revision identifiers, used by Alembic.
revision = '5e8358028b93'
down_revision = 'f7f8d9d25ab9'
branch_labels = None
depends_on = None


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


def fix_text(text: str) -> str: return text.replace("'", "’").replace(' :', ': ')


def parse_json_columns(column_name: str, object_class):
    names = []
    for x in mv[column_name]:
        for y in loads(x):
            obj = object_class(**y)
            if object_class == Country: obj.iso_3166_1 = obj.iso_3166_1.lower()
            obj.name = fix_text(obj.name)
            if obj.name not in names:
                names.append(obj.name)
                op.execute(f'INSERT INTO {object_class.__name__.lower()} VALUES {tuple(obj.__dict__.values())}')


def upgrade() -> None:
    column_args = [('production_countries', Country), ('spoken_languages', Language), ('genres', Genre), ('production_companies', Company), ('keywords', Keyword)]
    for index, status in enumerate(status_ar): op.execute(f"INSERT INTO status VALUES ({index}, '{status}')")
    for args in column_args: parse_json_columns(*args)
    spoken = [lang['iso_639_1'] for js in mv['spoken_languages'] for lang in loads(js)]
    for language in mv['original_language']:
        if language not in spoken: op.execute(f"INSERT INTO language VALUES ('{language}', '???')")


def downgrade() -> None:
    op.execute("""
        DELETE FROM status;
        DELETE FROM language;
        DELETE FROM genre;
        DELETE FROM keyword;
        DELETE FROM company;
        DELETE FROM country;
        """)
