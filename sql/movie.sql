set search_path = s3964_movie;

-- step 1 down
DROP TABLE IF EXISTS language CASCADE;
DROP TABLE IF EXISTS status CASCADE;
DROP TABLE IF EXISTS movie CASCADE;
DROP TABLE IF EXISTS department CASCADE;
DROP TABLE IF EXISTS gender CASCADE;
DROP TABLE IF EXISTS genre CASCADE;
DROP TABLE IF EXISTS job CASCADE;
DROP TABLE IF EXISTS crew CASCADE;
DROP TABLE IF EXISTS company CASCADE;
DROP TABLE IF EXISTS country CASCADE;
DROP TABLE IF EXISTS keyword CASCADE;
DROP TABLE IF EXISTS movie_company CASCADE;
DROP TABLE IF EXISTS movie_country CASCADE;
DROP TABLE IF EXISTS movie_cast CASCADE;
DROP TABLE IF EXISTS movie_crew CASCADE;
DROP TABLE IF EXISTS movie_keyword CASCADE;
DROP TABLE IF EXISTS movie_genre CASCADE;
DROP TABLE IF EXISTS movie_languages CASCADE;

-- step 1 up
CREATE TABLE language(
    iso_639_1 TEXT PRIMARY KEY,
    language_name TEXT NOT NULL UNIQUE
);

CREATE TABLE status(
    status_id SERIAL PRIMARY KEY,
    status_name TEXT NOT NULL UNIQUE
);

CREATE TABLE movie(
    movie_id SERIAL PRIMARY KEY,
    budget INT,
    english_title TEXT,
    homepage TEXT,
    original_language TEXT REFERENCES language(iso_639_1),
    original_title TEXT,
    overview TEXT,
    popularity DOUBLE PRECISION,
    release_date DATE,
    revenue INT,
    runtime INT,
    status INT REFERENCES status(status_id) ON DELETE CASCADE,
    tagline TEXT,
    vote_average FLOAT,
    vote_count INT
);

CREATE TABLE department(
    department_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    department_name TEXT NOT NULL UNIQUE
);

CREATE TABLE gender(
    gender_id SERIAL PRIMARY KEY,
    gender_name TEXT NOT NULL UNIQUE
);

CREATE TABLE genre(
    genre_id SERIAL PRIMARY KEY,
    genre_name TEXT NOT NULL UNIQUE
);

CREATE TABLE job(
    job_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    job_name TEXT NOT NULL UNIQUE
);

CREATE TABLE crew(
    credit_id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    department UUID REFERENCES department(department_id) ON DELETE CASCADE,
    gender INT REFERENCES gender(gender_id) ON DELETE CASCADE,
    job UUID REFERENCES job(job_id) ON DELETE CASCADE,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE company(
    company_id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL UNIQUE
);

CREATE TABLE country(
    iso_3166_1 TEXT PRIMARY KEY,
    country_name TEXT NOT NULL UNIQUE
);

CREATE TABLE keyword(
    keyword_id SERIAL PRIMARY KEY,
    keyword_name TEXT NOT NULL UNIQUE
);

CREATE TABLE movie_company(
    movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE,
    company_id INT REFERENCES company(company_id) ON DELETE CASCADE
);

CREATE TABLE movie_cast(
    cast_id SERIAL PRIMARY KEY,
    character TEXT NOT NULL UNIQUE,
    movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE,
    crew_id UUID REFERENCES crew(credit_id) ON DELETE CASCADE,
    credit_order INT
);

CREATE TABLE movie_crew(
    movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE,
    crew_id UUID REFERENCES crew(credit_id) ON DELETE CASCADE
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

CREATE TABLE movie_languages(
    movie_id INT REFERENCES movie(movie_id) ON DELETE CASCADE,
    language_id TEXT REFERENCES language(iso_639_1) ON DELETE CASCADE
);