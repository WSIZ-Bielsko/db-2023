"""

create table ecdsa_keys

Revision ID: 46e39f5ec448
Creation date: 2023-07-15 10:48:18.689545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "46e39f5ec448"
down_revision = "064bfd97e069"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE ECDSA_KEYS(
        key_id UUID default gen_random_uuid() PRIMARY KEY,
        key BYTEA NOT NULL, 
        pub BYTEA NOT NULL,
        owner_person_id UUID NOT NULL,
        created_at TIMESTAMP,
        invalid_after TIMESTAMP
    )
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS ECDSA_KEYS
    """)
