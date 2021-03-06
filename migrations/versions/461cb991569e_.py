"""empty message

Revision ID: 461cb991569e
Revises: 01fff29d4792
Create Date: 2020-02-12 23:18:35.580079

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '461cb991569e'
down_revision = '01fff29d4792'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tournament_match', sa.Column('round_match', sa.Integer(), nullable=False))
    op.alter_column('tournament_match', 'match_result_one',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('tournament_match', 'match_result_two',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.drop_column('tournament_match', 'round')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tournament_match', sa.Column('round', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.alter_column('tournament_match', 'match_result_two',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('tournament_match', 'match_result_one',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.drop_column('tournament_match', 'round_match')
    # ### end Alembic commands ###
