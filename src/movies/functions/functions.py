import json
from collections.abc import Iterable
import pandas as pd
from model import *

pd.options.display.max_rows = 10


# Actors
def get_cast():
    df = pd.read_csv('./datas/tmdb_5000_credits.csv')
    casts_ = list(df['cast'])
    return casts_


def get_cast_of_movie(movie_id: int, cast_field: str) -> list[CastEntry]:
    dicts = json.loads(cast_field)
    entries = []
    for d in dicts:
        entry = CastEntry(movie_id=movie_id, **d)
        entries.append(entry)
    return entries


def get_actors_of_movie(casts: list[str]) -> Iterable[Actor]:
    actors = []
    for a, movie in enumerate(casts):
        entries = get_cast_of_movie(a, movie)
        actors.extend([(e.id, e.name) for e in entries])
    actors = set(actors)
    return actors


# Crew
def get_crew():
    df = pd.read_csv('datas/tmdb_5000_credits.csv')
    crew_ = list(df['crew'])
    return crew_


def get_crew_of_movie(index: int, crew_field: str) -> list[CrewEntry]:
    dicts = json.loads(crew_field)
    entries = []
    for d in dicts:
        entry = CrewEntry(movie_index=index, **d)
        entries.append(entry)
    return entries


def get_crew_persons(crews: list) -> Iterable[CrewPerson]:
    people = []
    for c, movie in enumerate(crews):
        entries = get_crew_of_movie(c, movie)
        people.extend([(e.id, e.name) for e in entries])
    people = set(people)
    return people


def to_movie_crew(crew_entry: CrewEntry) -> MovieCrew:
    c = crew_entry
    return MovieCrew(movie_id=c.movie_index, person_id=c.id, credit_id=c.credit_id,
                     department=c.department, gender=c.gender, job=c.job)


# Movies
def get_movies(filename: str) -> Iterable[Movie]:
    df = pd.read_csv(filename)
    subframe = df.loc[:, ['id', 'title']]
    subframe_as_dict = subframe.to_dict(orient='records')
    movies = [Movie(movie_id=d['id'], title=d['title']) for d in subframe_as_dict]
    return movies


def get_movie_actors(filename: str) -> Iterable[MovieActor]:
    df = pd.read_csv(filename)
    subframe = df.loc[:, ['movie_id', 'cast']]
    subframe_as_dict = subframe.to_dict(orient='records')
    result = []
    for row in subframe_as_dict:
        movie_id = row['movie_id']
        cast_string = row['cast']
        all_casts = get_cast_of_movie(movie_id, cast_string)
        all_casts = [to_movie_actor(ac) for ac in all_casts]
        result.extend(all_casts)
    return result


def to_movie_actor(cast_entry: CastEntry) -> MovieActor:
    c = cast_entry
    return MovieActor(movie_id=c.movie_id, actor_id=c.id, cast_id=c.cast_id,
                      character=c.character, credit_id=c.credit_id, gender=c.gender,
                      orders=c.order)


def get_movie_crew(filename: str) -> Iterable[MovieCrew]:
    df = pd.read_csv(filename)
    subframe = df.loc[:, ['movie_id', 'crew']]
    subframe_as_dict = subframe.to_dict(orient='records')
    result = []
    for row in subframe_as_dict:
        movie_id = row['movie_id']
        crew = row['crew']
        all_crew = get_crew_of_movie(movie_id, crew)
        all_crew = [to_movie_crew(ac) for ac in all_crew]
        result.extend(all_crew)

    return result


if __name__ == '__main__':
    cdf = pd.read_csv('./datas/tmdb_5000_credits.csv')
    casts_ = list(cdf['cast'])

    print(casts_)
