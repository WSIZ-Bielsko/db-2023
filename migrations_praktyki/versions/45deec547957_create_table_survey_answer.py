"""

create_table_survey_answer

Revision ID: 45deec547957
Creation date: 2023-07-24 15:56:27.311629

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "45deec547957"
down_revision = "ed20b1549b1e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE survey_answer (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            survey_id uuid NOT NULL,
            category INT NOT NULL,
            question TEXT NOT NULL,
            score INT NOT NULL, 
            CONSTRAINT category_id FOREIGN KEY (survey_id) REFERENCES survey(id) ON DELETE NO ACTION
        )
        """)


def downgrade() -> None:
    op.execute('drop table if exists survey_answer')
