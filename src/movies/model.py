from dataclasses import dataclass


# {'cast_id': 102, 'character': 'Ambient Room Tech / Troupe', 'credit_id': '52fe48019251416c750acb6f',
# 'gender': 1, 'id': 42286, 'name': 'Julene Renee', 'order': 82}

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


# {'credit_id': '573c8e2f9251413f5d000094', 'department': 'Crew', 'gender': 1,
# 'id': 1621932, 'job': 'Stunts', 'name': 'Min Windle'}

@dataclass
class CrewEntry:
    movie_id: int
    credit_id: str  # unique?
    department: str
    gender: int
    id: int  # id of ... the person?
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
