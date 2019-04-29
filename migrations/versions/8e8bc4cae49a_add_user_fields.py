"""add user fields

Revision ID: 8e8bc4cae49a
Revises: 61ac758788d5
Create Date: 2019-04-01 18:02:40.600318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e8bc4cae49a'
down_revision = '61ac758788d5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('card_brand', sa.Text(), nullable=True))
    op.add_column('user', sa.Column('last_4', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_4')
    op.drop_column('user', 'card_brand')
    # ### end Alembic commands ###