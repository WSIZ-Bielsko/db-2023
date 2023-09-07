"""

create table curriculum_vitae

Revision ID: 9c189d643d47
Creation date: 2023-07-21 14:18:11.227634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9c189d643d47"
down_revision = "5e545acad71a"
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("""
    CREATE TABLE curriculum_vitae(
        id UUID default gen_random_uuid() PRIMARY KEY,
        student_id UUID NOT NULL,
        data bytea NOT NULL,
        created_at TIMESTAMP NOT NULL,
        immutable bool DEFAULT False
    )
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS curriculum_vitae
    """)
    pass
