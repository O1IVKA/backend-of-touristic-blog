from datetime import datetime

from fastapi_users.db.sqlalchemy import GUID
from pydantic import validator
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, sql, Boolean, Table
from sqlalchemy.orm import relationship, backref
from app.users.models import UserTable
from core.db import Base

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    slug = Column(String, unique=True)
    title = Column(String(350))
    description = Column(String)
    text = Column(String(350))
    date = Column(DateTime(timezone=True), server_default=sql.func.now())
    is_active = Column(Boolean, default=True)

    user_id = Column(GUID, ForeignKey('user.id'))
    user = relationship(UserTable, backref="post")

    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship("City", backref="post")

    comment = relationship("Comment", back_populates="post")

    likes = relationship('PostLike', backref='post', lazy='dynamic')

    tag = relationship("Tag", secondary='post_tag', back_populates="post")
    image = Column(String)

    def __repr__(self):
        return f"<Post: {self.title}>"


class PostLike(Base):
    __tablename__ = 'post_like'
    id = Column(Integer, primary_key=True)
    user_id = Column(GUID, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))


class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    is_active = Column(Boolean, default=True)
    date = Column(DateTime(), default=datetime.utcnow, index=True)

    parent_id = Column(Integer, ForeignKey('comment.id'))
    replies = relationship('Comment', backref=backref('parent', remote_side=[id]))

    user_id = Column(GUID, ForeignKey("user.id"))
    user = relationship(UserTable, back_populates="comment")

    post_id = Column(Integer, ForeignKey("post.id"))
    post = relationship("Post", back_populates="comment")

    def __repr__(self):
        return f"<Comment: {self.text}>"


post_tag = Table(
    'post_tag', Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String)

    post = relationship('Post', secondary=post_tag, back_populates='tag')

