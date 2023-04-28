"""

patch

Revision ID: 469a91635a5a
Creation date: 2023-04-22 12:18:41.235145

"""
from pandas import read_csv
from alembic import op
from dataclasses import dataclass
from sqlalchemy.exc import IntegrityError

# revision identifiers, used by Alembic.
revision = '469a91635a5a'
down_revision = 'b255657cc105'
branch_labels = None
depends_on = None

cr = read_csv('/home/user/Projects/db/migrations/data/tmdb_5000_credits.csv')
def fix_text(text: str) -> str: return text.replace("'", "’")


@dataclass
class Cast:
    cast_id: int
    character: str
    credit_id: str
    gender: int
    id: int
    name: str
    order: int


def upgrade() -> None:
    from uuid import uuid4
    from json import loads
    ids = []
    cast_uuid = uuid4()
    length = len(cr['cast'])
    op.execute(f"INSERT INTO job VALUES ('{cast_uuid}', 'Cast')")
    for index, casts in enumerate(cr['cast']):
        for cast in loads(casts):
            c = Cast(**cast)
            if c.id not in ids:
                ids.append(c.id)
                if index % 1000 == 0: print(f'Progress: {round(index*100/length,2)}%')
                op.execute(f"INSERT INTO actor SELECT {c.id}, {c.gender}, '{fix_text(c.name)}', '{c.credit_id}' WHERE NOT EXISTS(SELECT 1 FROM actor WHERE actor_id = {c.id})")


def downgrade() -> None:
    op.execute('DELETE FROM actors;')
