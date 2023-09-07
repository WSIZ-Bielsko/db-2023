"""

create table documents

Revision ID: 993007bf8a74
Creation date: 2023-07-13 10:57:16.326442

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "993007bf8a74"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        create table documents (
            id UUID default gen_random_uuid() primary key,
            created_at TIMESTAMP NOT NULL,
            json_repr BYTEA,
            filename TEXT, 
            data BYTEA,
            sha256 TEXT NOT NULL
        );
        """
    )


def downgrade() -> None:
    op.execute("drop table documents")
