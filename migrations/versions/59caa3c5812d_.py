"""empty message

Revision ID: 59caa3c5812d
Revises: 7944ed16acd6
Create Date: 2020-01-02 00:54:43.667883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '59caa3c5812d'
down_revision = '7944ed16acd6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('answer', 'answers',
               existing_type=sa.VARCHAR(length=200),
               type_=sa.String(length=500),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('answer', 'answers',
               existing_type=sa.String(length=500),
               type_=sa.VARCHAR(length=200),
               existing_nullable=True)
    # ### end Alembic commands ###
