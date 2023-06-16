"""create table video_views

Revision ID: 1763b143d9ca
Revises: da12c1a1d125
Create Date: 2023-06-16 16:33:54.048992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1763b143d9ca'
down_revision = 'da12c1a1d125'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE video_views(
    video_id UUID NOT NULL REFERENCES video(video_id),
    channel_id UUID NOT NULL REFERENCES channel(channel_id)
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE video_views')
