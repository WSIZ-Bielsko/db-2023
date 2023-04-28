"""

create_table_part_2

Revision ID: f7f8d9d25ab9
Creation date: 2023-04-15 15:02:56.786352

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'f7f8d9d25ab9'
down_revision = 'be6936b207ec'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
CREATE TABLE company(
    company_id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL
);

CREATE TABLE country(
    iso_3166_1 TEXT PRIMARY KEY,
    country_name TEXT NOT NULL
);

CREATE TABLE keyword(
    keyword_id SERIAL PRIMARY KEY,
    keyword_name TEXT NOT NULL
);

CREATE TABLE movie_company(
    movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE,
    company_id INT REFERENCES company(company_id) ON DELETE CASCADE
);

CREATE TABLE movie_cast(
    cast_id SERIAL PRIMARY KEY,
    character TEXT NOT NULL,
    movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE,
    crew_id INT REFERENCES crew(crew_id) ON DELETE CASCADE,
    credit_order INT
);

CREATE TABLE movie_crew(
    movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE,
    crew_id INT REFERENCES crew(crew_id) ON DELETE CASCADE
);

CREATE TABLE movie_country(
    movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE,
    country_id TEXT REFERENCES country(iso_3166_1) ON DELETE CASCADE
);

CREATE TABLE movie_genre(
    movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE,
    genre_id INT REFERENCES genre(genre_id) ON DELETE CASCADE
);

CREATE TABLE movie_keyword(
    movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE,
    keyword_id INT REFERENCES keyword(keyword_id) ON DELETE CASCADE
);

CREATE TABLE movie_language(
    movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE,
    language_id TEXT REFERENCES language(iso_639_1) ON DELETE CASCADE
);
    """)


def downgrade() -> None:
    op.execute("""
DROP TABLE IF EXISTS company CASCADE;
DROP TABLE IF EXISTS country CASCADE;
DROP TABLE IF EXISTS keyword CASCADE;
DROP TABLE IF EXISTS movie_company CASCADE;
DROP TABLE IF EXISTS movie_country CASCADE;
DROP TABLE IF EXISTS movie_cast CASCADE;
DROP TABLE IF EXISTS movie_crew CASCADE;
DROP TABLE IF EXISTS movie_keyword CASCADE;
DROP TABLE IF EXISTS movie_genre CASCADE;
DROP TABLE IF EXISTS movie_language CASCADE;
    """)
