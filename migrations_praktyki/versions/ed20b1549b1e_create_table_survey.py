"""

create_table_survey

Revision ID: ed20b1549b1e
Creation date: 2023-07-21 21:14:46.093758

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "ed20b1549b1e"
down_revision = "a68e3cea52b6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        create table survey (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            internship_period_id UUID NOT NULL,
            final_score FLOAT NOT NULL, 
            submitted_at TIMESTAMP,
            submitted BOOLEAN DEFAULT false
        );
        """
    )


def downgrade() -> None:
    op.execute('drop table if exists survey')
