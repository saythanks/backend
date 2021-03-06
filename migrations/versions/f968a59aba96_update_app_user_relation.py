"""update app user relation

Revision ID: f968a59aba96
Revises: 3816d9f71747
Create Date: 2019-03-03 17:50:29.467627

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f968a59aba96"
down_revision = "3816d9f71747"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "app_user",
        sa.Column(
            "id",
            postgresql.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
    )

    role_t = sa.Enum("user", "admin", name="role_t")
    role_t.create(op.get_bind())

    op.add_column(
        "app_user", sa.Column("role", role_t, server_default="admin", nullable=False)
    )
    op.add_column(
        "app_user",
        sa.Column(
            "time_created",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "app_user",
        sa.Column(
            "time_udpated",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.drop_constraint("app_user_app_id_fkey", "app_user", type_="foreignkey")
    op.create_foreign_key(None, "app_user", "user", ["app_id"], ["id"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "app_user", type_="foreignkey")
    op.execute("DROP TYPE role_t;")
    op.create_foreign_key("app_user_app_id_fkey", "app_user", "app", ["app_id"], ["id"])
    op.drop_column("app_user", "time_udpated")
    op.drop_column("app_user", "time_created")
    op.drop_column("app_user", "role")
    op.drop_column("app_user", "id")
    # ### end Alembic commands ###
