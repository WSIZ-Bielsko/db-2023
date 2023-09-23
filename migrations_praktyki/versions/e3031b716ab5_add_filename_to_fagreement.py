"""

add filename to fagreement

Revision ID: e3031b716ab5
Creation date: 2023-08-07 11:25:03.717072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e3031b716ab5"
down_revision = "f50f9f3b151a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    alter table framework_agreements add column file_name text default 'umowa.pdf'
    """)


def downgrade() -> None:
    op.execute("""
    alter table framework_agreements drop column file_name
    """)
