"""create table playlist

Revision ID: 6eedb582d219
Revises: 02ef95a37fe2
Create Date: 2023-06-16 16:35:16.474065

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6eedb582d219'
down_revision = '02ef95a37fe2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE playlist(
    playlist_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
    playlist_name TEXT NOT NULL CHECK(playlist_name ~ '^[ -~]{1,50}$'),
    playlist_owner_id UUID NOT NULL REFERENCES channel(channel_id),
    created TIMESTAMP DEFAULT NOW() NOT NULL CHECK(created <= edited),
    edited TIMESTAMP DEFAULT NOW() NOT NULL CHECK(edited >= created)
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE playlist')