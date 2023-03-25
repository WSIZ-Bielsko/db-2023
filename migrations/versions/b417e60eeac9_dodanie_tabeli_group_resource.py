"""

dodanie tabeli group_resource

Revision ID: b417e60eeac9
Creation date: 2023-03-25 11:07:43.943898

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = 'b417e60eeac9'
down_revision = 'fb9ee3520c95'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
create table group_resource(
    groupid uuid unique references securitygroup(groupid) on delete cascade,
    resourceid uuid unique references securedresources(resourceid) on delete cascade
);
alter table group_resource add constraint pk_resourcegroup primary key (groupid, resourceid);
        """
    )


def downgrade() -> None:
    op.execute(
        """
alter table group_resource drop constraint pk_resourcegroup;
drop table group_resource;
        """
    )
