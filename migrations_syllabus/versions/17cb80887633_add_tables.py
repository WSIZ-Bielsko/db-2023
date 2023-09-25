"""

add_tables

Revision ID: 17cb80887633
Creation date: 2023-09-22 17:05:07.508205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17cb80887633'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE lecture(
        lecture_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
        lecture_name TEXT UNIQUE
    );
    
    CREATE TABLE lecturer(
        lecturer_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
        lecturer_name TEXT UNIQUE
    );
    
    CREATE TABLE semester(
        semester_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
        semester_name TEXT UNIQUE,
        semester_start DATE DEFAULT NOW(),
        semester_end DATE DEFAULT NOW() CHECK (semester_end >= semester_start)
    );
    
    CREATE TABLE syllabus(
        syllabus_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
        lecture_id UUID REFERENCES lecture(lecture_id) ON DELETE CASCADE,
        semester_id UUID REFERENCES semester(semester_id) ON DELETE CASCADE,
        lecturer_id UUID REFERENCES lecturer(lecturer_id) ON DELETE CASCADE
    );
    
    CREATE TABLE lecture_content(
        content_id UUID DEFAULT GEN_RANDOM_UUID() PRIMARY KEY,
        order_number INT,
        syllabus_id UUID REFERENCES syllabus(syllabus_id) ON DELETE CASCADE,
        lecture_topic TEXT NOT NULL,
        UNIQUE (order_number, syllabus_id)
    );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE lecture CASCADE;
    DROP TABLE lecturer CASCADE;
    DROP TABLE semester CASCADE;
    DROP TABLE syllabus CASCADE;
    DROP TABLE lecture_content CASCADE;
    """)
