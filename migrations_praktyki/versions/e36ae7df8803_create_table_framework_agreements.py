"""

create table framework_agreements

Revision ID: e36ae7df8803
Creation date: 2023-07-25 13:08:52.789853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e36ae7df8803"
down_revision = "24bcb297e410"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE framework_agreements (
        id UUID default gen_random_uuid() PRIMARY KEY,
        company_id UUID NOT NULL,
        active BOOL DEFAULT TRUE,
        created_at DATE NOT NULL,
        file_data BYTEA
    )
    """)


def downgrade() -> None:
    op.execute('drop table if exists framework_agreements')
