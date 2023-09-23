"""

create table companies

Revision ID: 0413105a2d32
Creation date: 2023-07-24 13:27:16.937507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0413105a2d32"
down_revision = "9c189d643d47"
branch_labels = None
depends_on = None


# class Company(BaseModel):
#     company_id: UUID
#     name: str
#     info: str | None
#     nip: str  # number; but might be international

def upgrade() -> None:
    op.execute("""
    CREATE TABLE companies(
        id UUID default gen_random_uuid() PRIMARY KEY,
        name text NOT NULL,
        info text,
        nip text NOT NULL
    )
    """)
    pass


def downgrade() -> None:
    op.execute('DROP TABLE if exists companies')
    pass
