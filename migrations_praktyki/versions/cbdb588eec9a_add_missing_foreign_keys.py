"""

add_missing_foreign_keys

Revision ID: cbdb588eec9a
Creation date: 2023-09-07 20:47:17.957808

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'cbdb588eec9a'
down_revision = 'ffafefc9a15e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE applications ADD CONSTRAINT FK1 FOREIGN KEY (student_id) REFERENCES persons;
    ALTER TABLE applications ADD CONSTRAINT FK2 FOREIGN KEY (cv_id) REFERENCES curriculum_vitae;
    ALTER TABLE audit_log ADD CONSTRAINT FK1 FOREIGN KEY (author_of_log) REFERENCES persons;
    ALTER TABLE audit_log ADD CONSTRAINT FK2 FOREIGN KEY (target_of_log) REFERENCES persons;
    ALTER TABLE curriculum_vitae ADD CONSTRAINT FK1 FOREIGN KEY (student_id) REFERENCES persons;
    ALTER TABLE days ADD CONSTRAINT FK1 FOREIGN KEY (period_id) REFERENCES internship_periods;
    ALTER TABLE ecdsa_keys ADD CONSTRAINT FK1 FOREIGN KEY (owner_person_id) REFERENCES persons;
    ALTER TABLE internships ADD CONSTRAINT FK1 FOREIGN KEY (student_id) REFERENCES persons;
    ALTER TABLE internship_agreements ADD CONSTRAINT FK1 FOREIGN KEY (student_id) REFERENCES persons;
    ALTER TABLE internship_agreements ADD CONSTRAINT FK2 FOREIGN KEY (application_id) REFERENCES applications;
    ALTER TABLE internship_periods ADD agreement_id UUID;
    ALTER TABLE internship_periods ADD CONSTRAINT FK1 FOREIGN KEY (agreement_id) REFERENCES internship_agreements;
    ALTER TABLE internship_periods ADD CONSTRAINT FK2 FOREIGN KEY (student_id) REFERENCES persons;
    ALTER TABLE period_final_reports ADD CONSTRAINT FK1 FOREIGN KEY (student_id) REFERENCES persons;
    ALTER TABLE period_final_reports ADD CONSTRAINT FK2 FOREIGN KEY (period_id) REFERENCES internship_periods;
    ALTER TABLE signatures ADD CONSTRAINT FK1 FOREIGN KEY (person_id) REFERENCES persons;
    ALTER TABLE signature_texts ADD CONSTRAINT FK1 FOREIGN KEY (person_id) REFERENCES persons;
    ALTER TABLE survey ADD CONSTRAINT FK1 FOREIGN KEY (internship_period_id) REFERENCES internship_periods;
    """)


def downgrade() -> None:
    op.execute("""
    ALTER TABLE applications DROP CONSTRAINT FK1 CASCADE;
    ALTER TABLE applications DROP CONSTRAINT FK2 CASCADE;
    ALTER TABLE audit_log DROP CONSTRAINT FK1 CASCADE;
    ALTER TABLE audit_log DROP CONSTRAINT FK2 CASCADE;
    ALTER TABLE curriculum_vitae DROP CONSTRAINT FK1;
    ALTER TABLE days DROP CONSTRAINT FK1 CASCADE;
    ALTER TABLE ecdsa_keys DROP CONSTRAINT FK1;
    ALTER TABLE internships DROP CONSTRAINT FK1 CASCADE;
    ALTER TABLE internship_agreements DROP CONSTRAINT FK1 CASCADE;
    ALTER TABLE internship_agreements DROP CONSTRAINT FK2 CASCADE;
    ALTER TABLE internship_periods DROP CONSTRAINT FK1 CASCADE;
    ALTER TABLE internship_periods DROP CONSTRAINT FK2 CASCADE;
    ALTER TABLE period_final_reports DROP CONSTRAINT FK1 CASCADE;
    ALTER TABLE period_final_reports DROP CONSTRAINT FK2 CASCADE;
    ALTER TABLE signatures DROP CONSTRAINT FK1 CASCADE;
    ALTER TABLE signature_texts DROP CONSTRAINT FK1 CASCADE;
    ALTER TABLE survey DROP CONSTRAINT FK1 CASCADE;
    """)
