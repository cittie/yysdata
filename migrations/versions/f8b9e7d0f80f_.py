"""empty message

Revision ID: f8b9e7d0f80f
Revises: 
Create Date: 2017-03-15 18:02:42.130000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8b9e7d0f80f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shikigamis',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('rarity', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('souls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('missions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('mission_type', sa.Integer(), nullable=True),
    sa.Column('stamina_cost', sa.Integer(), nullable=True),
    sa.Column('soul_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['soul_id'], ['souls.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reward_quests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('shikigami_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['shikigami_id'], ['shikigamis.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reward_quests')
    op.drop_table('missions')
    op.drop_table('souls')
    op.drop_table('shikigamis')
    # ### end Alembic commands ###
