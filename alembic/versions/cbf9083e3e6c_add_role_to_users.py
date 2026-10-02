"""add role to users

Revision ID: cbf9083e3e6c
Revises: c8af08902897
Create Date: 2026-10-01 21:06:01.503181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cbf9083e3e6c'
down_revision: Union[str, Sequence[str], None] = 'c8af08902897'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_role_enum = sa.Enum(
        "CUSTOMER",
        "SELLER",
        "ADMIN",
        name="userrole",
    )

    user_role_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role_enum,
            nullable=False,
            server_default="CUSTOMER",
        ),
    )

def downgrade() -> None:
    op.drop_column("users", "role")

    user_role_enum = sa.Enum(
        "CUSTOMER",
        "SELLER",
        "ADMIN",
        name="userrole",
    )

    user_role_enum.drop(op.get_bind(), checkfirst=True)
