"""

create table access_tokens

Revision ID: da92dd8cf06c
Creation date: 2023-07-28 15:36:25.491155

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "da92dd8cf06c"
down_revision = "f823ee4f375a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""--sql
        CREATE TABLE access_tokens(
            token UUID NOT NULL,
            person_id UUID NOT NULL,

            created_at TIMESTAMP WITH TIME ZONE NOT NULL,
            CONSTRAINT fk_user FOREIGN KEY(person_id) REFERENCES persons(person_id) ON DELETE CASCADE
        );
        """)


def downgrade() -> None:
    op.execute('drop table if exists access_tokens')
