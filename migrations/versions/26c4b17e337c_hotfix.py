"""hotfix

Revision ID: 26c4b17e337c
Revises: f968a59aba96
Create Date: 2019-03-03 18:06:37.262531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26c4b17e337c'
down_revision = 'f968a59aba96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('app_user_app_id_fkey', 'app_user', type_='foreignkey')
    op.create_foreign_key(None, 'app_user', 'app', ['app_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'app_user', type_='foreignkey')
    op.create_foreign_key('app_user_app_id_fkey', 'app_user', 'user', ['app_id'], ['id'])
    # ### end Alembic commands ###