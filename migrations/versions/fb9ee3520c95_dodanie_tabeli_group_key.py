"""

dodanie tabeli group_key

Revision ID: fb9ee3520c95
Creation date: 2023-03-25 11:07:38.304615

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'fb9ee3520c95'
down_revision = '7479ce452579'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
create table group_key(
    groupid uuid references securitygroup(groupid) on delete cascade,
    keyid uuid references accesskey(keyid) on delete cascade
);
alter table group_key add constraint pk_group primary key (groupid, keyid);
        """
    )

def downgrade() -> None:
    op.execute(
        """
alter table group_key drop constraint pk_group;
drop table group_key;
        """
    )