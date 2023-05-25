import json
from collections.abc import Collection

import pandas as pd

from model import *

pd.options.display.max_rows = 10


def get_cast_of_movie(index: int, cast_field: str) -> list[CastEntry]:
    dicts = json.loads(cast_field)
    entries = []
    for d in dicts:
        entry = CastEntry(movie_index=index, **d)
        entries.append(entry)
    return entries


def get_crew_of_movie(movie_id: int, crew_field: str) -> list[Crew]:
    dicts = json.loads(crew_field)
    entries = []
    for d in dicts:
        entry = Crew(movie_id=movie_id, **d)
        entries.append(entry)
    return entries


def get_actors(filename: str) -> Collection[Actor]:
    casts = get_casts(filename)
    actors = []
    for i, movie in enumerate(casts):
        entries = get_cast_of_movie(i, movie)
        actors.extend([(c.id, c.name) for c in entries])
    actors = set(actors)
    return [Actor(*a) for a in actors]


def to_movie_actor(cast_entry: CastEntry) -> MovieActor:
    c = cast_entry
    return MovieActor(movie_id=c.movie_index, actor_id=c.id, cast_id=c.cast_id, credit_id=c.credit_id,
                      character=c.character, gender=c.gender, position=c.order)


def get_movie_actors(filename: str) -> Collection[MovieActor]:
    df_ = pd.read_csv(filename)
    df_sub = df_.loc[:, ['movie_id', 'cast']]  # wycinek tabel
    df_as_dict = df_sub.to_dict(orient='records')

    res = []
    for row in df_as_dict:
        movie_id = row['movie_id']
        cast_as_str = row['cast']
        entries: list[CastEntry] = get_cast_of_movie(movie_id, cast_as_str)

        movie_actors = [to_movie_actor(c) for c in entries]
        res.extend(movie_actors)

    return res


def get_movies(filename: str) -> Collection[Movie]:
    df_ = pd.read_csv(filename)
    df_sub = df_.loc[:, ['id', 'title', 'budget', 'popularity', 'release_date', 'revenue']]  # wycinek tabel
    df_as_dict = df_sub.to_dict(orient='records')
    movies = []
    for d in df_as_dict:
        rdate = d['release_date']
        try:
            release_date = datetime.strptime(str(rdate), '%Y-%m-%d').date()
        except ValueError as e:
            print(rdate)
            continue
        m = Movie(movie_id=d['id'], title=d['title'], budget=d['budget'], popularity=d['popularity'],
                  release_date=release_date, revenue=d['revenue'] / 1000)
        movies.append(m)
    return movies


def get_casts(filename: str) -> list[str]:
    df_ = pd.read_csv(filename)
    return list(df_['cast'])


def get_crews(filename: str) -> list[Crew]:
    df_ = pd.read_csv(filename)
    w = df_.loc[:, ['movie_id', 'crew']]
    df_as_dict = w.to_dict(orient='records')
    all_crew = []
    for d in df_as_dict:
        movie_id = int(d['movie_id'])
        crews = get_crew_of_movie(movie_id, d['crew'])
        all_crew.extend(crews)
    return all_crew


def get_genres(filename: str) -> Collection[Genre]:
    df_ = pd.read_csv(filename)
    genres = list(df_['genres'])  # list[str]
    entries = set()
    for genre in genres:
        dicts = json.loads(genre)
        for d in dicts:
            entry = Genre(genre_id=d['id'], name=d['name'])
            entries.add(entry)
    return entries


def get_movie_genres(filename) -> Collection[MovieGenre]:
    df_ = pd.read_csv(filename)
    df_sub = df_.loc[:, ['id', 'genres']]  # wycinek tabel
    df_as_dict = df_sub.to_dict(orient='records')
    entries = set()
    for movie in df_as_dict:
        genres = json.loads(movie.get('genres'))
        for genre in genres:
            entry = MovieGenre(movie_id=movie.get('id'), genre_id=genre['id'])
            entries.add(entry)

    return entries


def get_pcountries(filename) -> Collection[PCountry]:
    df_ = pd.read_csv(filename)
    pcountries = list(df_['production_countries'])  # list[str]

    res = set()
    for pcountry in pcountries:
        dicts = json.loads(pcountry)
        for d in dicts:
            pcountry = PCountry(iso_3166_1=d['iso_3166_1'], name=d['name'])
            res.add(pcountry)
    return res


def get_movie_pcountries(filename):
    df = pd.read_csv(filename)
    df_sub = df.loc[:, ['id', 'production_countries']]  # wycinek tabel
    df_as_dict = df_sub.to_dict(orient='records')
    entries = []
    for movie in df_as_dict:
        pcountries = json.loads(movie.get('production_countries'))
        for pcountry in pcountries:
            entry = MoviePCountry(movie_id=movie.get('id'), iso_3166_1=pcountry['iso_3166_1'])
            entries.append(entry)

    return entries


if __name__ == '__main__':
    crews = get_crews('data/tmdb_5000_credits.csv')
    cids = set()
    for c in crews:
        cids.add(c.credit_id)
    print(len(crews))
    print(len(cids))  # equal
