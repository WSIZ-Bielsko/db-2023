"""

create table signatures

Revision ID: e69103e1d546
Creation date: 2023-07-17 09:12:56.118909

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "e69103e1d546"
down_revision = "46e39f5ec448"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE SIGNATURES(
        id UUID default gen_random_uuid() PRIMARY KEY,
        document_id UUID NOT NULL, 
        signature_text_id UUID NOT NULL, 
        person_id UUID NOT NULL, 
        person_roles_at_signing integer[],
        type int, 
        signed_at timestamp,
        data bytea,
        keyid UUID 
    )
    """)


def downgrade() -> None:
    op.execute('drop table if exists signatures')
