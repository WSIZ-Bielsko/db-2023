"""

create table signature_texts

Revision ID: 67d359af9480
Creation date: 2023-07-17 09:46:26.051057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "67d359af9480"
down_revision = "e69103e1d546"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE SIGNATURE_TEXTS(
        id UUID default gen_random_uuid() PRIMARY KEY,
        document_id UUID NOT NULL,
        person_id UUID NOT NULL,
        document_sha256 text NOT NULL, 
        verbal text NOT NULL
    )
    """)


def downgrade() -> None:
    op.execute('drop table if exists signature_texts')
