"""

create table movie countries

Revision ID: 555cb0f59599
Creation date: 2023-04-29 12:51:31.966929

"""
from alembic import op, context


# revision identifiers, used by Alembic.
revision = '555cb0f59599'
down_revision = 'd2f971ee984c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
   CREATE TABLE movie_countries(
        movie_id INT,
        country_id VARCHAR(3),
        
        CONSTRAINT fk_movie_id FOREIGN KEY (movie_id)
        REFERENCES movies(movie_id),
        CONSTRAINT fk_country_id FOREIGN KEY (country_id)
        REFERENCES countries(country_id)  
        );
    """)


def downgrade() -> None:
    op.execute("""
     DROP TABLE IF EXISTS movie_countries CASCADE;
    """)
