"""empty message

Revision ID: ef62bf7618eb
Revises: 0939dc75ffcc
Create Date: 2023-03-13 16:34:33.294461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef62bf7618eb'
down_revision = '0939dc75ffcc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('units', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_insurance', sa.Integer(), nullable=True))
        batch_op.drop_constraint('units_id_Insurance_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'insurance', ['id_insurance'], ['id'])
        batch_op.drop_column('id_Insurance')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('units', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_Insurance', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('units_id_Insurance_fkey', 'insurance', ['id_Insurance'], ['id'])
        batch_op.drop_column('id_insurance')

    # ### end Alembic commands ###