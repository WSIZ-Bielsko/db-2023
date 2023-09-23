"""

create period_final_report

Revision ID: 934db09a34cd
Creation date: 2023-07-24 21:49:35.821699

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "934db09a34cd"
down_revision = "6ad2a8868019"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE period_final_reports(
        id UUID default gen_random_uuid() PRIMARY KEY,
        period_id UUID NOT NULL,
        period_days UUID[] NOT NULL,
        total_days int,
        student_id UUID NOT NULL,
        company_id UUID NOT NULL,
        created_at TIMESTAMP NOT NULL
    )
    """)


def downgrade() -> None:
    op.execute('drop table if exists period_final_reports')
