"""

dodanie tabeli accesskey

Revision ID: 09f8a606a458
Creation date: 2023-03-25 11:05:48.761909

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '09f8a606a458'
down_revision = '8f2cc22eb003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        create table accesskey(
            keyid UUID DEFAULT gen_random_uuid() primary key,
            name text not null unique
        );
        """
    )
def downgrade() -> None:
    op.execute(
        """
        drop table accesskey;        
        """
    )
