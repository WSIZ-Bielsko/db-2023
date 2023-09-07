"""

create internship_agreements

Revision ID: 9547ad6adcc6
Creation date: 2023-07-21 09:45:06.782557

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "9547ad6adcc6"
down_revision = "6e6714bb323d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE internship_agreements (
        id UUID default gen_random_uuid() PRIMARY KEY,
        created_at TIMESTAMP NOT NULL, 
        application_id UUID NOT NULL,
        company_id UUID NOT NULL,
        student_id UUID NOT NULL
    )
    """)


def downgrade() -> None:
    op.execute('drop table if exists internship_agreements')
