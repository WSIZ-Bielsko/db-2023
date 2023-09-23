"""

cereate_table_survey_question

Revision ID: a68e3cea52b6
Creation date: 2023-07-24 15:40:56.910077

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "a68e3cea52b6"
down_revision = "0413105a2d32"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE survey_question (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            category INT NOT NULL, 
            question TEXT NOT null
        )
        """)


def downgrade() -> None:
    op.execute('drop table if exists survey_question')
