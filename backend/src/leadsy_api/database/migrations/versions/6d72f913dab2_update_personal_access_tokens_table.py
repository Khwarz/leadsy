"""Update personal access tokens table

Revision ID: 6d72f913dab2
Revises: cf00905f57a1
Create Date: 2023-08-10 07:57:57.093726

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6d72f913dab2"
down_revision = "cf00905f57a1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "personal_access_tokens", sa.Column("expires_at", sa.DateTime(), nullable=True)
    )
    op.drop_constraint(
        "personal_access_tokens_user_id_fkey",
        "personal_access_tokens",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "user_token_fk",
        "personal_access_tokens",
        "users",
        ["user_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("user_token_fk", "personal_access_tokens", type_="foreignkey")
    op.create_foreign_key(
        "personal_access_tokens_user_id_fkey",
        "personal_access_tokens",
        "users",
        ["user_id"],
        ["id"],
    )
    op.drop_column("personal_access_tokens", "expires_at")
    # ### end Alembic commands ###
