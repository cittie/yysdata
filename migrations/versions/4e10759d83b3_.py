"""empty message

Revision ID: 4e10759d83b3
Revises: f8b9e7d0f80f
Create Date: 2017-03-15 19:26:04.282000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e10759d83b3'
down_revision = 'f8b9e7d0f80f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shikigamis',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('rarity', sa.String(length=4), nullable=True),
    sa.Column('awaken_materials', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('souls',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('position', sa.Integer(), nullable=True),
    sa.Column('attr_2_pieces', sa.String(length=64), nullable=True),
    sa.Column('attr_4_pieces', sa.String(length=256), nullable=True),
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
