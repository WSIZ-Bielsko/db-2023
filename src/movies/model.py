from dataclasses import dataclass
from datetime import datetime, date


# {'cast_id': 102, 'character': 'Ambient Room Tech / Troupe', 'credit_id': '52fe48019251416c750acb6f',
# 'gender': 1, 'id': 42286, 'name': 'Julene Renee', 'order': 82}

@dataclass(frozen=True)
class CastEntry:
    movie_index: int  # dodane... rząd w csv-ie
    cast_id: int
    character: str
    credit_id: str
    gender: int
    id: int  # id of ... the actor?
    name: str
    order: int


@dataclass(frozen=True)
class MovieActor:
    cast_id: int
    movie_id: int
    actor_id: int
    credit_id: str
    character: str
    gender: int
    position: int


# {'credit_id': '573c8e2f9251413f5d000094', 'department': 'Crew', 'gender': 1, 'id': 1621932,
# 'job': 'Stunts', 'name': 'Min Windle'}

@dataclass
class Crew:
    credit_id: str  # unique
    movie_id: int   # credit_id → (single, unique) movie_id ---> *:1 relation (no need for join-table)
    department: str
    gender: int
    id: int  # id of ... the person?
    job: str
    name: str


@dataclass(frozen=True)
class Movie:
    movie_id: int
    title: str
    budget: int
    popularity: float
    release_date: date
    revenue: int


@dataclass(frozen=True)
class Actor:
    actor_id: int
    name: str


# "[{""id"": 28, ""name"": ""Action""}, {""id"": 12, ""name"": ""Adventure""},
#   {""id"": 14, ""name"": ""Fantasy""}, {""id"": 878, ""name"": ""Science Fiction""}]"
@dataclass(frozen=True)
class Genre:
    genre_id: int
    name: str


@dataclass(frozen=True)
class MovieGenre:
    movie_id: int
    genre_id: int


@dataclass(frozen=True)
class PCountry:
    iso_3166_1: str
    name: str


@dataclass(frozen=True)
class MoviePCountry:
    movie_id: int
    iso_3166_1: str
