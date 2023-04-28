from dataclasses import dataclass
from datetime import datetime


@dataclass
class CastEntry:
    movie_id: int  # dodane... rząd w csv-ie
    id: int  # id of the actor
    cast_id: int
    character: str
    credit_id: str
    gender: int
    name: str
    order: int

@dataclass
class MovieActor:
    movie_id: int  # dodane... rząd w csv-ie
    actor_id: int  # id of the actor
    cast_id: int
    character: str
    credit_id: str
    gender: int
    order_: int


@dataclass
class CrewEntry:
    movie_id: int
    credit_id: str  # unique?
    department: str
    gender: int
    id: int
    job: str
    name: str

@dataclass
class Actor:
    actor_id: int
    name: str


@dataclass
class Movie:
    movie_id: int
    title: str