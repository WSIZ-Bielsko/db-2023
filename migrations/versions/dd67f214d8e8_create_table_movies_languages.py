"""

create table movies languages

Revision ID: dd67f214d8e8
Creation date: 2023-04-29 12:41:39.185712

"""
from alembic import op, context

# revision identifiers, used by Alembic.
revision = 'dd67f214d8e8'
down_revision = 'e6d1ba467e61'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE movie_languages (
        movie_id INT NOT NULL,
        lang_id VARCHAR(2) NOT NULL,
        
        CONSTRAINT fk_movie_id FOREIGN KEY (movie_id)
            REFERENCES movies(movie_id),
        CONSTRAINT fk_lang_id FOREIGN KEY (lang_id)
            REFERENCES languages(lang_id)    
    );
    """)


def downgrade() -> None:
    op.execute("""
    DROP TABLE IF EXISTS movie_languages CASCADE;
    """)
