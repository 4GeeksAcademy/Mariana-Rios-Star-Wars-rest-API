"""empty message

Revision ID: 66a4879b33a9
Revises: 4cbb4f99a0d6
Create Date: 2023-11-01 22:14:19.119291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '66a4879b33a9'
down_revision = '4cbb4f99a0d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('character',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('gender', sa.String(length=250), nullable=True),
    sa.Column('height', sa.String(length=250), nullable=True),
    sa.Column('mass', sa.String(length=250), nullable=True),
    sa.Column('hair_color', sa.String(length=250), nullable=True),
    sa.Column('eye_color', sa.String(length=250), nullable=True),
    sa.Column('skin_color', sa.String(length=250), nullable=True),
    sa.Column('birth_year', sa.String(length=250), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('characters')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('image_url', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('name', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('gender', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('height', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('hair_color', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('eye_color', sa.VARCHAR(length=250), autoincrement=False, nullable=True),
    sa.Column('birth_year', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='characters_pkey')
    )
    op.drop_table('character')
    # ### end Alembic commands ###
