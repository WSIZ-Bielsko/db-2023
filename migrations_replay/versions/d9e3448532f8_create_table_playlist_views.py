"""create table playlist_views

Revision ID: d9e3448532f8
Revises: 8c5f241ae2f7
Create Date: 2023-06-16 16:35:25.201603

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd9e3448532f8'
down_revision = '8c5f241ae2f7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE playlist_views(
    playlist_id UUID NOT NULL UNIQUE REFERENCES playlist(playlist_id),
    channel_id UUID NOT NULL UNIQUE REFERENCES channel(channel_id)
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE playlist_views CASCADE')
