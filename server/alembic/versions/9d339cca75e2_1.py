"""1

Revision ID: 9d339cca75e2
Revises: 
Create Date: 2020-12-10 09:09:43.435985

"""
import fastapi_users
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d339cca75e2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(length=350), nullable=True),
    sa.Column('text', sa.String(length=350), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_country_id'), 'country', ['id'], unique=True)
    op.create_table('tags',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tags_id'), 'tags', ['id'], unique=True)
    op.create_table('city',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(length=350), nullable=True),
    sa.Column('text', sa.String(length=350), nullable=True),
    sa.Column('country_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['country_id'], ['country.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_city_id'), 'city', ['id'], unique=True)
    op.create_table('user',
                    sa.Column('id', fastapi_users.db.sqlalchemy.GUID(), nullable=False),
                    sa.Column('email', sa.String(length=320), nullable=False),
                    sa.Column('hashed_password', sa.String(length=72), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('is_superuser', sa.Boolean(), nullable=False),
                    sa.Column('full_name', sa.String(length=255), nullable=True),
                    sa.Column('image', sa.String(), nullable=True),
                    sa.Column('city_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['city_id'], ['city.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slug', sa.String(), nullable=True),
    sa.Column('title', sa.String(length=350), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('text', sa.String(length=350), nullable=True),
    sa.Column('date', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('user_id', fastapi_users.db.sqlalchemy.GUID(), nullable=True),
    sa.Column('city_id', sa.Integer(), nullable=True),
    sa.Column('image', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['city_id'], ['city.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_index(op.f('ix_post_id'), 'post', ['id'], unique=True)
    op.create_table('user_to_user',
    sa.Column('follower_id', fastapi_users.db.sqlalchemy.GUID(), nullable=False),
    sa.Column('followed_id', fastapi_users.db.sqlalchemy.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('follower_id', 'followed_id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('user_id', fastapi_users.db.sqlalchemy.GUID(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comment_date'), 'comment', ['date'], unique=False)
    op.create_index(op.f('ix_comment_id'), 'comment', ['id'], unique=False)
    op.create_table('post_like',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', fastapi_users.db.sqlalchemy.GUID(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_tag',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
    sa.PrimaryKeyConstraint('post_id', 'tag_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_tag')
    op.drop_table('post_like')
    op.drop_index(op.f('ix_comment_id'), table_name='comment')
    op.drop_index(op.f('ix_comment_date'), table_name='comment')
    op.drop_table('comment')
    op.drop_table('user_to_user')
    op.drop_index(op.f('ix_post_id'), table_name='post')
    op.drop_table('post')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_city_id'), table_name='city')
    op.drop_table('city')
    op.drop_index(op.f('ix_tags_id'), table_name='tags')
    op.drop_table('tags')
    op.drop_index(op.f('ix_country_id'), table_name='country')
    op.drop_table('country')
    # ### end Alembic commands ###
