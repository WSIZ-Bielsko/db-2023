"""

adding_constraints

Revision ID: a71bb8772f7a
Creation date: 2023-09-09 12:37:55.968532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a71bb8772f7a'
down_revision = 'cbdb588eec9a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE survey ADD CONSTRAINT UN01 UNIQUE (internship_period_id);
    ALTER TABLE applications ADD CONSTRAINT UN02 UNIQUE (framework_agreement_id);
    ALTER TABLE internship_agreements ADD CONSTRAINT UN03 UNIQUE (application_id);
    ALTER TABLE days ADD CONSTRAINT UN04 UNIQUE (period_id, date_at);
    ALTER TABLE ecdsa_keys ADD CONSTRAINT UN05 UNIQUE (key);
    ALTER TABLE internships ADD CONSTRAINT UN06 UNIQUE (student_id);
    ALTER TABLE persons ADD CONSTRAINT UN07 UNIQUE (company_id, uid_in_company);
    ALTER TABLE period_final_reports ADD CONSTRAINT UN08 UNIQUE (period_id);
    ALTER TABLE signature_texts ADD CONSTRAINT UN09 UNIQUE (document_id, person_id);
    ALTER TABLE signatures ADD CONSTRAINT UN10 UNIQUE (document_id, person_id);
    """)


def downgrade() -> None:
    op.execute("""
    ALTER TABLE survey DROP CONSTRAINT UN01 CASCADE;
    ALTER TABLE applications DROP CONSTRAINT UN02 CASCADE;
    ALTER TABLE internship_agreements DROP CONSTRAINT UN03 CASCADE;
    ALTER TABLE days DROP CONSTRAINT UN04 CASCADE;
    ALTER TABLE ecdsa_keys DROP CONSTRAINT UN05 CASCADE;
    ALTER TABLE internships DROP CONSTRAINT UN06 CASCADE;
    ALTER TABLE persons DROP CONSTRAINT UN07 CASCADE;
    ALTER TABLE period_final_reports DROP CONSTRAINT UN08 CASCADE;
    ALTER TABLE signature_texts DROP CONSTRAINT UN09 CASCADE;
    ALTER TABLE signatures DROP CONSTRAINT UN10 CASCADE;
    """)
