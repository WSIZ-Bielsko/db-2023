"""

create table persons

Revision ID: af62bdbdd8db
Creation date: 2023-07-13 19:11:57.623299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "af62bdbdd8db"
down_revision = "993007bf8a74"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        create table persons (
            person_id UUID default gen_random_uuid() primary key,
            name TEXT NOT NULL, 
            email TEXT, 
            phone TEXT,
            studentid INT, 
            album TEXT,
            wykladowcaid INT,
            company_id UUID, 
            uid_in_company UUID,
            roles integer[]
        );
        """
    )


def downgrade() -> None:
    op.execute('drop table persons')

