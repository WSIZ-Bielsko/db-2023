from dataclasses import dataclass
from uuid import UUID
from datetime import datetime


@dataclass
class Region:
    region_id: UUID | None
    region_name: str


@dataclass
class ElectionType:
    type_id: UUID | None
    type_name: str
    no_of_choices: int


@dataclass
class Election:
    election_id: UUID | None
    type_id: UUID
    region_id: UUID
    vote_start: datetime
    vote_end: datetime


@dataclass
class Choice:
    choice_id: UUID | None
    choice_name: str
    image: str


@dataclass
class Token:
    token_id: UUID | None
    election_id: str


@dataclass
class Voter:
    voter_id: UUID | None
    voter_name: str


class TokenAlreadyAssigned(RuntimeError):
    pass


class AccessDenied(TokenAlreadyAssigned):
    pass


class InvalidVote(AccessDenied):
    pass
