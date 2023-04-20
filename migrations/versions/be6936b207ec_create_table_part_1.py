"""

create_table_part_1

Revision ID: be6936b207ec
Creation date: 2023-04-15 15:02:47.579922

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'be6936b207ec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE language(
        iso_639_1 TEXT PRIMARY KEY,
        language_name TEXT NOT NULL
    );

    CREATE TABLE status(
        status_id SERIAL PRIMARY KEY,
        status_name TEXT NOT NULL
    );

    CREATE TABLE movie(
        movie_id SERIAL PRIMARY KEY,
        budget BIGINT,
        english_title TEXT,
        homepage TEXT,
        original_language TEXT REFERENCES language(iso_639_1) ON DELETE CASCADE ,
        original_title TEXT,
        overview TEXT,
        popularity DOUBLE PRECISION,
        release_date DATE,
        revenue BIGINT,
        runtime INT,
        status INT REFERENCES status(status_id) ON DELETE CASCADE,
        tagline TEXT,
        vote_average FLOAT,
        vote_count BIGINT
    );

    CREATE TABLE department(
        department_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        department_name TEXT NOT NULL
    );

    CREATE TABLE gender(
        gender_id SERIAL PRIMARY KEY,
        gender_name TEXT NOT NULL
    );

    CREATE TABLE genre(
        genre_id SERIAL PRIMARY KEY,
        genre_name TEXT NOT NULL
    );

    CREATE TABLE job(
        job_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        job_name TEXT NOT NULL
    );

    CREATE TABLE crew(
        crew_id SERIAL PRIMARY KEY,
        department UUID REFERENCES department(department_id) ON DELETE CASCADE,
        gender INT REFERENCES gender(gender_id) ON DELETE CASCADE,
        job UUID REFERENCES job(job_id) ON DELETE CASCADE,
        name TEXT NOT NULL,
        credit_id TEXT NOT NULL
    );
        """)


def downgrade() -> None:
    op.execute("""
DROP TABLE IF EXISTS language CASCADE;
DROP TABLE IF EXISTS status CASCADE;
DROP TABLE IF EXISTS movie CASCADE;
DROP TABLE IF EXISTS department CASCADE;
DROP TABLE IF EXISTS gender CASCADE;
DROP TABLE IF EXISTS genre CASCADE;
DROP TABLE IF EXISTS job CASCADE;
DROP TABLE IF EXISTS crew CASCADE;
""")
