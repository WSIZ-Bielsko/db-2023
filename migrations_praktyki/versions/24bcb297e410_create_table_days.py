"""

create table days

Revision ID: 24bcb297e410
Creation date: 2023-07-25 12:50:34.861881

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "24bcb297e410"
down_revision = "934db09a34cd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE days (
        id UUID default gen_random_uuid() PRIMARY KEY,
        period_id UUID NOT NULL,
        date_at DATE NOT NULL,
        immutable BOOL DEFAULT FALSE,
        project TEXT DEFAULT '',
        tasks TEXT[]
    )
    """)


def downgrade() -> None:
    op.execute('drop table if exists days')
