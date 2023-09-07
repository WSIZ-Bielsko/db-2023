"""

create table audit_log

Revision ID: 064bfd97e069
Creation date: 2023-07-17 13:28:59.280998

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "064bfd97e069"
down_revision = "af62bdbdd8db"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        create table audit_log (
            id UUID default gen_random_uuid() primary key,
            time_of_log TIMESTAMP NOT NULL,
            author_of_log UUID NOT NULL,
            target_of_log UUID NOT NULL,
            log_message TEXT NOT NULL
        );
        """)


# author_of_log UUID REFERENCES persons(person_id),
# target_of_log UUID REFERENCES persons(person_id),     todo: held here for a 'future migration'

def downgrade() -> None:
    op.execute("drop table audit_log")
