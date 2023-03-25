"""

dodanie tabeli securedresources

Revision ID: addb751fbadf
Creation date: 2023-03-25 11:05:58.021199

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'addb751fbadf'
down_revision = '09f8a606a458'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        create table securedresources(
            resourceid UUID DEFAULT gen_random_uuid() primary key,
            name text not null unique,
            isopen bool default true not null
        );
        """
    )


def downgrade() -> None:
    op.execute(
        """
        drop table securedresources;
        """
    )