"""

create table applications

Revision ID: 6e6714bb323d
Creation date: 2023-07-19 15:56:48.836667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6e6714bb323d"
down_revision = "a1a75aaa309c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE APPLICATIONS(
        id UUID default gen_random_uuid() PRIMARY KEY,
        framework_agreement_id UUID NOT NULL,
        company_id UUID NOT NULL,
        cv_id UUID, 
        student_id UUID NOT NULL,
        info text
    )
    """)


def downgrade() -> None:
    op.execute('drop table if exists applications')
