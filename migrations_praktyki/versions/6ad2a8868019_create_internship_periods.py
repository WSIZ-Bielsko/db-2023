"""

create internship_periods

Revision ID: 6ad2a8868019
Creation date: 2023-07-21 17:14:56.972815

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "6ad2a8868019"
down_revision = "45deec547957"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE internship_periods (
        id UUID default gen_random_uuid() PRIMARY KEY,
        internship_id UUID NOT NULL,
        student_id UUID NOT NULL,
        company_id UUID NOT NULL,
        
        status INT,
        
        opened_at TIMESTAMP,
        expected_end TIMESTAMP
    )
    """)


def downgrade() -> None:
    op.execute('drop table if exists internship_periods')
