"""create table video

Revision ID: d84325290942
Revises: 9dfbc69d2a88
Create Date: 2023-06-16 16:33:34.505561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd84325290942'
down_revision = '9dfbc69d2a88'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE video(
    video_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
    title TEXT NOT NULL CHECK(title ~ '^[ -~]{1,50}$'),
    owner UUID NOT NULL REFERENCES channel(channel_id),
    filename TEXT NOT NULL CHECK(filename ~ '^[ -~]{1,255}$'),
    description TEXT NOT NULL CHECK(title ~ '^[ -~]{1,100}$'),
    created TIMESTAMP DEFAULT NOW() NOT NULL CHECK(created <= edited),
    edited TIMESTAMP DEFAULT NOW() NOT NULL CHECK(edited >= created)
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE video;')
