"""create table playlist_video

Revision ID: 8c5f241ae2f7
Revises: 6eedb582d219
Create Date: 2023-06-16 16:35:19.174307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c5f241ae2f7'
down_revision = '6eedb582d219'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE playlist_video(
    playlist_id UUID NOT NULL UNIQUE REFERENCES playlist(playlist_id),
    video_id UUID NOT NULL UNIQUE REFERENCES video(video_id)
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE playlist_video CASCADE')
