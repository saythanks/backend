"""db updates

Revision ID: 7a54afb8c6f2
Revises: 70fa9d7fdb16
Create Date: 2019-04-22 01:44:05.881362

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7a54afb8c6f2'
down_revision = '70fa9d7fdb16'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('time_updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.alter_column('account', 'balance',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('account', 'time_udpated')
    op.add_column('app', sa.Column('time_updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.drop_column('app', 'time_udpated')
    op.add_column('app_user', sa.Column('time_updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.drop_column('app_user', 'time_udpated')
    op.add_column('deposit', sa.Column('time_updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.drop_column('deposit', 'time_udpated')
    op.add_column('payable', sa.Column('time_updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.drop_column('payable', 'time_udpated')
    op.add_column('payment', sa.Column('time_updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.drop_column('payment', 'time_udpated')
    op.add_column('user', sa.Column('time_updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.drop_column('user', 'time_udpated')
    op.add_column('withdrawal', sa.Column('time_updated', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.drop_column('withdrawal', 'time_udpated')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('withdrawal', sa.Column('time_udpated', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.drop_column('withdrawal', 'time_updated')
    op.add_column('user', sa.Column('time_udpated', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.drop_column('user', 'time_updated')
    op.add_column('payment', sa.Column('time_udpated', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.drop_column('payment', 'time_updated')
    op.add_column('payable', sa.Column('time_udpated', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.drop_column('payable', 'time_updated')
    op.add_column('deposit', sa.Column('time_udpated', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.drop_column('deposit', 'time_updated')
    op.add_column('app_user', sa.Column('time_udpated', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.drop_column('app_user', 'time_updated')
    op.add_column('app', sa.Column('time_udpated', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.drop_column('app', 'time_updated')
    op.add_column('account', sa.Column('time_udpated', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False))
    op.alter_column('account', 'balance',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('account', 'time_updated')
    # ### end Alembic commands ###
