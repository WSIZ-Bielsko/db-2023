"""

create internships

Revision ID: 5e545acad71a
Creation date: 2023-07-21 09:45:14.389655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5e545acad71a"
down_revision = "9547ad6adcc6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE internships (
        id UUID default gen_random_uuid() PRIMARY KEY,
        student_id UUID,
        total_days int DEFAULT 0,
        start_at DATE,
        closed_at DATE
    )
    """)


def downgrade() -> None:
    op.execute('drop table if exists internships')
