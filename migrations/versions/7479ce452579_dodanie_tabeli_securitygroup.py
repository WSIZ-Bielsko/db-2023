"""

dodanie tabeli securitygroup

Revision ID: 7479ce452579
Creation date: 2023-03-25 11:06:02.665853

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '7479ce452579'
down_revision = 'addb751fbadf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        create table securitygroup(
    groupid UUID DEFAULT gen_random_uuid() not null primary key,
    groupname text not null unique
);
        """
    )
def downgrade() -> None:
    op.execute(
        """
drop table securitygroup;
        """
    )