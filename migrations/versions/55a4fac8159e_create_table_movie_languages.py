"""create table movielanguages

Revision ID: 55a4fac8159e
Revises: b687107fac13
Create Date: 2023-04-24 08:16:05.569887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55a4fac8159e'
down_revision = 'b687107fac13'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(f"""
    --sql 
    CREATE TABLE movie_languages (
        movie_id INT NOT NULL,
        lang_id VARCHAR(2) NOT NULL,
        
        CONSTRAINT fk_movie_id FOREIGN KEY (movie_id)
            REFERENCES movies(movie_id),
        CONSTRAINT fk_lang_id FOREIGN KEY (lang_id)
            REFERENCES languages(lang_id)    
    )

""")


def downgrade() -> None:
    op.execute(f"""
    DROP TABLE IF EXISTS movie_languages CASCADE;
""")
