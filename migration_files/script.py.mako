"""

${message}

Revision ID: ${up_revision}
Creation date: ${create_date}

"""
from alembic import op, context
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else ""}

    if "seed" in context.get_x_argument(as_dictionary=True):
        seed()


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}


def seed() -> None:
    seeds = []

    for seed in seeds:
        pass
