"""

insert_values_from_movies_csv_part_3

Revision ID: b12cc75770ed
Creation date: 2023-04-18 16:49:31.719249

"""
from alembic import op
from pandas import read_csv

# revision identifiers, used by Alembic.
revision = 'b12cc75770ed'
down_revision = '10e187a765da'
branch_labels = None
depends_on = None

mv = read_csv('/home/user/Projects/db/migrations/data/tmdb_5000_movies.csv')


def upgrade() -> None:
    from json import loads
    column_args = [('production_companies', 'company'), ('spoken_languages', 'language'), ('production_countries', 'country'), ('genres', 'genre'), ('keywords', 'keyword')]
    for column, table in column_args:
        zipped = list(zip(mv['id'], mv[column]))
        for movie_id, elements in zipped:
            element_ids = [list(x.values())[1 if table == 'company' else 0] for x in loads(elements)]
            for element_id in element_ids:
                print(f'movie_{table} - {element_id}')
                element_id = element_id if isinstance(element_id, int) else element_id.lower()
                op.execute(f'INSERT INTO movie_{table} VALUES {(movie_id, element_id)}')


def downgrade() -> None:
    op.execute("""
    DELETE FROM movie_company;
    DELETE FROM movie_country;
    DELETE FROM movie_genre;
    DELETE FROM movie_keyword;
    DELETE FROM movie_language;
    """)
