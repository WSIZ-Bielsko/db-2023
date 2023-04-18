"""

insert values from credits.csv part 1

Revision ID: 2bcd2bba1262
Creation date: 2023-04-19 01:06:31.694259

"""
from pandas import read_csv
from alembic import op
from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Crew:
    id: int
    department: UUID
    gender: int
    job: UUID
    name: str
    credit_id: str


# revision identifiers, used by Alembic.
revision = '2bcd2bba1262'
down_revision = 'b12cc75770ed'
branch_labels = None
depends_on = None

cr = read_csv('/home/user/Projects/db/migrations/data/tmdb_5000_credits.csv')


def fix_text(text: str) -> str: return text.replace("'", "’")


def check_value(obj, field: str, table: dict):
    name = obj.__getattribute__(field)
    if name not in table:
        uuid = generate_random_uuid(table)
        op.execute(f"INSERT INTO {field} VALUES ('{uuid}', '{fix_text(name)}')")
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
    for crews in cr['crew']:
        for crew in loads(crews):
            c = Crew(**crew)
            if c.id not in ids:
                ids.append(c.id)
                check_value(c, 'department', departments)
                check_value(c, 'job', jobs)
                op.execute(f"INSERT INTO crew VALUES ('{c.id}', '{c.department}', {c.gender}, '{c.job}', '{fix_text(c.name)}', '{c.credit_id}')")


def downgrade() -> None:
    op.execute("""
    DELETE FROM gender;
    DELETE FROM department;
    DELETE FROM job;
    DELETE FROM crew;
    """)
