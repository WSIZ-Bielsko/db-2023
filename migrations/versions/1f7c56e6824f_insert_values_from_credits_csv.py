"""

insert values from credits.csv

Revision ID: 1f7c56e6824f
Creation date: 2023-04-18 21:58:47.322059

"""
from pandas import read_csv
from alembic import op
from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Crew:
    credit_id: UUID
    department: UUID
    gender: int
    job: UUID
    name: str
    id: int


@dataclass
class Cast:
    cast_id: int
    character: str
    credit_id: str
    gender: int
    id: int
    name: str
    order: int


# revision identifiers, used by Alembic.
revision = '1f7c56e6824f'
down_revision = 'b12cc75770ed'
branch_labels = None
depends_on = None

cr = read_csv('/home/user/Projects/db/migrations/data/tmdb_5000_credits.csv')


def check_value(obj, field: str, table: dict):
    name = obj.__getattribute__(field)
    if name not in table:
        uuid = generate_random_uuid(table)
        op.execute(f"INSERT INTO {field} VALUES ('{uuid}', '{name}')")
        table[name] = uuid
        obj.__setattr__(field, uuid)
    else: obj.__setattr__(field, table[name])


def generate_random_uuid(uuid_dict: dict) -> UUID:
    uuid = uuid4()
    while uuid in uuid_dict: uuid = uuid4()
    return uuid


def upgrade() -> None:
    genders = ['Unknown', 'Female', 'Male']
    for index, gender in enumerate(genders): op.execute(f"INSERT INTO gender VALUES ({index}, '{gender}')")
    from json import loads
    departments, jobs, ids = {}, {}, []
    for index, crews in enumerate(cr['crew']):
        movie_id = cr['movie_id'][index]
        for crew in loads(crews):
            c = Crew(**crew)
            if c.id not in ids:
                ids.append(c.id)
                check_value(c, 'department', departments)
                check_value(c, 'job', jobs)
                c.name = c.name.replace("'", "\"")
                op.execute(f"INSERT INTO crew VALUES ('{c.id}', '{c.department}', {c.gender}, '{c.job}', '{c.name}')")
                op.execute(f"INSERT INTO movie_crew VALUES ({movie_id}, '{c.id}')")
    ids.clear()
    for index, casts in enumerate(cr['cast']):
        movie_id = cr['movie_id'][index]
        for cast in loads(casts):
            c = Cast(**cast)
            if c.id not in ids:
                ids.append(c.id)
                op.execute(f"INSERT INTO movie_cast VALUES ({c.cast_id}, {c.name}, {movie_id}, {c.id}, {c.order})")


def downgrade() -> None:
    op.execute("""
    DELETE FROM gender;
    DELETE FROM department;
    DELETE FROM job;
    DELETE FROM crew;
    DELETE FROM movie_cast;
    DELETE FROM movie_crew;
    """)
