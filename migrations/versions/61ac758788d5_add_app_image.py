"""add app image

Revision ID: 61ac758788d5
Revises: d95b8447a36e
Create Date: 2019-04-01 00:19:38.826466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61ac758788d5'
down_revision = 'd95b8447a36e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('app', sa.Column('image_url', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('app', 'image_url')
    # ### end Alembic commands ###
