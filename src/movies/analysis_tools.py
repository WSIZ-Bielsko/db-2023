import json
from collections import defaultdict
from collections.abc import Iterable

import pandas as pd

from src.movies.model import CastEntry, Actor, Movie, MovieActor


# pd.options.display.max_rows = 10


def get_cast_of_movie(movie_id: int, cast_field: str) -> list[CastEntry]:
    dicts = json.loads(cast_field)
    entries = []
    for d in dicts:
        entry = CastEntry(movie_id=movie_id, **d)
        entries.append(entry)
    return entries

def to_movie_actor(cast_entry: CastEntry) -> MovieActor:
    e = cast_entry
    return MovieActor(movie_id=e.movie_id, actor_id=e.id, cast_id=e.cast_id, character=e.character,
                      credit_id=e.credit_id, gender=e.gender, order_=e.order)


def check_unique_cast_creditid(casts: list[str]):
    credit_ids = []
    for i, movie in enumerate(casts):
        entries = get_cast_of_movie(i, movie)
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


def get_actors(casts: list[str]) -> Iterable[Actor]:
    actors = []
    for i, movie in enumerate(casts):
        entries = get_cast_of_movie(i, movie)
        actors.extend([(c.id, c.name) for c in entries])
    actors = set(actors)
    return actors


def get_movies(filename: str) -> Iterable[Movie]:
    df = pd.read_csv(filename)
    df_sub = df.loc[:, ['id', 'title']]  # wycinek tabel
    df_as_dict = df_sub.to_dict(orient='records')
    movies = [Movie(movie_id=d['id'], title=d['title']) for d in df_as_dict]
    return movies

def get_movieactors(filename: str) -> list[MovieActor]:
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
        if len(v) > 1:
            print('name->ids ', k, v)

if __name__ == '__main__':
    df = pd.read_csv('../../migrations/data/tmdb_5000_credits.csv')

def get_casts():
    df = pd.read_csv('data/tmdb_5000_credits.csv')
    casts_ = list(df['cast'])  # list[str]
    return casts_


if __name__ == '__main__':
    casts_ = get_casts()

    # check_unique_cast_creditid(casts_)
    # check_assignment_actor_actorid(casts_)
    # find_duplicates(casts_)
    # c = get_actors(casts_)
    # movies = get_movies('data/tmdb_5000_movies.csv')
    movieactors = get_movieactors('data/tmdb_5000_credits.csv')
    for m in movieactors:
        print(m)
    print(len(movieactors))
    # for c in movies:
    #     print(c)
