import json
from collections import defaultdict
from collections.abc import Iterable

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


def get_crew_of_movie(index: int, crew_field: str) -> list[CrewEntry]:
    dicts = json.loads(crew_field)
    entries = []
    for d in dicts:
        entry = CrewEntry(movie_index=index, **d)
        entries.append(entry)
    return entries


def check_unique_cast_creditid(casts: list[str]):
    credit_ids = []
    for i, movie in enumerate(casts):
        entries = get_cast_of_movie(i, movie)
        credit_ids.extend([c.credit_id for c in entries])

    unique = (len(credit_ids) == len(set(credit_ids)))
    print(f'{unique=}')


def check_unique_crew_creditid(casts: list[str]):
    credit_ids = []
    for i, movie in enumerate(casts):
        entries = get_crew_of_movie(i, movie)
        credit_ids.extend([c.credit_id for c in entries])

    unique = (len(credit_ids) == len(set(credit_ids)))
    print(f'{unique=}')


def check_assignment_actor_actorid(casts: list[str]):
    name_id_pairs = []
    for i, movie in enumerate(casts):
        entries = get_cast_of_movie(i, movie)
        for e in entries:
            print(e)
        name_id_pairs.extend([(c.id, c.name) for c in entries])

    unique_pairs = set(name_id_pairs)
    n_pairs = len(unique_pairs)
    n_names = len(set([c for i, c in unique_pairs]))  # unique names
    n_ids = len(set([i for i, c in unique_pairs]))  # unique id's

    print(f'{n_pairs=}')
    print(f'{n_ids=}')
    print(f'{n_names=}')


def find_duplicates(casts: list[str]):
    name_id_pairs = []
    for i, movie in enumerate(casts):
        entries = get_cast_of_movie(i, movie)
        name_id_pairs.extend([(c.id, c.name) for c in entries])

    unique_pairs = set(name_id_pairs)
    id_to_name = defaultdict(lambda: set())
    for (id, name) in unique_pairs:
        id_to_name[id].add(name)

    for (k, v) in id_to_name.items():
        if len(v) > 1:
            print('id->names ', k, v)

    # -----
    name_to_id = defaultdict(lambda: set())
    for (id, name) in unique_pairs:
        name_to_id[name].add(id)

    for (k, v) in name_to_id.items():
        if len(v) > 4:
            print('name->ids ', k, v)


def find_duplicates_crew(crews: list[str]):
    name_id_pairs = []
    for i, movie in enumerate(crews):
        entries = get_crew_of_movie(i, movie)
        name_id_pairs.extend([(c.id, c.name) for c in entries])

    unique_pairs = set(name_id_pairs)
    id_to_name = defaultdict(lambda: set())
    for (id, name) in unique_pairs:
        id_to_name[id].add(name)

    for (k, v) in id_to_name.items():
        if len(v) > 1:
            print('id->names ', k, v)

    # -----
    name_to_id = defaultdict(lambda: set())
    for (id, name) in unique_pairs:
        name_to_id[name].add(id)

    for (k, v) in name_to_id.items():
        if len(v) > 4:
            print('name->ids ', k, v)


def get_actors(casts: list[str]) -> Iterable[Actor]:
    actors = []
    for i, movie in enumerate(casts):
        entries = get_cast_of_movie(i, movie)
        actors.extend([(c.id, c.name) for c in entries])
    actors = set(actors)
    return actors


def get_movie_actors(filename: str) -> Iterable[MovieActor]:
    df = pd.read_csv(filename)
    df_sub = df.loc[:, ['movie_id', 'cast']]  # wycinek tabel
    df_as_dict = df_sub.to_dict(orient='records')

    res = []
    for row in df_as_dict:
        movie_id = row['movie_id']
        cast_as_str = row['cast']
        all_casts = get_cast_of_movie(movie_id, cast_as_str)
        all_casts = [to_movie_actor(c) for c in all_casts]
        res.extend(all_casts)

    return res


def to_movie_actor(cast_entry: CastEntry) -> MovieActor:
    c = cast_entry
    return MovieActor(movie_id=c.movie_index, actor_id=c.id, cast_id=c.cast_id, credit_id=c.credit_id,
                      character=c.character, gender=c.gender, position=c.order)


def get_movies(filename: str) -> Iterable[Movie]:
    df = pd.read_csv(filename)
    df_sub = df.loc[:, ['id', 'title']]  # wycinek tabel
    df_as_dict = df_sub.to_dict(orient='records')
    movies = [Movie(movie_id=d['id'], title=d['title']) for d in df_as_dict]
    return movies


def get_casts():
    df = pd.read_csv('data/tmdb_5000_credits.csv')
    casts_ = list(df['cast'])  # list[str]
    return casts_


def get_genres():
    df = pd.read_csv('data/tmdb_5000_movies.csv')
    genres = list(df['genres'])  # list[str]
    entries = []
    for genre in genres:
        dicts = json.loads(genre)
        for d in dicts:
            entry = Genre(genre_id=d['id'], name=d['name'])
            if entry not in entries:
                entries.append(entry)
    return entries


def get_movie_genres(filename) -> set[MovieGenre]:
    df = pd.read_csv(filename)
    df_sub = df.loc[:, ['id', 'genres']]  # wycinek tabel
    df_as_dict = df_sub.to_dict(orient='records')
    entries = set()
    for movie in df_as_dict:
        genres = json.loads(movie.get('genres'))
        for genre in genres:
            entry = MovieGenre(movie_id=movie.get('id'), genre_id=genre['id'])
            entries.add(entry)

    return entries


def get_pcountries() -> list[PCountry]:
    df = pd.read_csv('data/tmdb_5000_movies.csv')
    pcountries = list(df['production_countries'])  # list[str]
    entries = []
    for pcountry in pcountries:
        dicts = json.loads(pcountry)
        for d in dicts:
            entry = PCountry(iso_3166_1=d['iso_3166_1'], name=d['name'])
            if entry not in entries:
                entries.append(entry)
    return entries


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
    # df = pd.read_csv('data/tmdb_5000_credits.csv')
    # casts_ = list(df['cast'])  # list[str]
    # crews_ = list(df['crew'])  # list[str]
    # check_unique_cast_creditid(casts_)
    # check_unique_crew_creditid(crews_)
    # check_assignment_actor_actorid(casts_)
    # find_duplicates_crew(crews_)
    print(len(get_movie_pcountries('data/tmdb_5000_movies.csv')))
