"""empty message

Revision ID: de1d7d7c0e79
Revises: bb616cf645db
Create Date: 2024-09-06 18:24:59.805656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'de1d7d7c0e79'
down_revision = 'bb616cf645db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('user_fk', 'user', ['user'], ['id'])

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('user_fk', 'user', ['user'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_constraint('user_fk', type_='foreignkey')
        batch_op.drop_column('user')

    with op.batch_alter_table('comments', schema=None) as batch_op:
        batch_op.drop_constraint('user_fk', type_='foreignkey')
        batch_op.drop_column('user')

    # ### end Alembic commands ###
