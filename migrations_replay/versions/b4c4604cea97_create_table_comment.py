"""create table comment

Revision ID: b4c4604cea97
Revises: a59fb02eae9e
Create Date: 2023-06-16 16:34:48.014608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b4c4604cea97'
down_revision = 'a59fb02eae9e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE comment(
    comment_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
    author UUID NOT NULL REFERENCES channel(channel_id),
    content TEXT NOT NULL CHECK(content ~ '^[ -~]{1,}$' and length(content) < 500),
    video_id UUID NOT NULL REFERENCES video(video_id),
    parent_comment UUID REFERENCES comment(comment_id) CHECK(parent_comment != comment_id),
    created TIMESTAMP DEFAULT NOW() NOT NULL CHECK(created <= edited),
    edited TIMESTAMP DEFAULT NOW() NOT NULL CHECK(edited >= created)
    );""")


def downgrade() -> None:
    op.execute('DROP TABLE comment')
