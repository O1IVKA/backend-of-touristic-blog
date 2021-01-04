from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users.db.sqlalchemy import GUID
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Table, ForeignKey, Integer

from core.db import Base

# First column holds the user who follows, the second the user who is being followed.
user_to_user = Table(
    'user_to_user', Base.metadata,
    Column("follower_id", GUID, ForeignKey("user.id"), primary_key=True),
    Column("followed_id", GUID, ForeignKey("user.id"), primary_key=True)
)


class UserTable(Base, SQLAlchemyBaseUserTable):
    full_name = Column(String(255))
    image = Column(String)

    comment = relationship("Comment", back_populates="user")
    city_id = Column(Integer, ForeignKey('city.id'))
    city = relationship("City", backref="user")
    liked = relationship('PostLike',
                         foreign_keys='PostLike.user_id',
                         backref='user', lazy='dynamic'
                         )

    following = relationship("UserTable",
                             secondary="user_to_user",
                             primaryjoin="UserTable.id==user_to_user.c.follower_id",
                             secondaryjoin="UserTable.id==user_to_user.c.followed_id",
                             backref="followers"
                             )

    def __repr__(self):
        return f"<UserTable: {self.email}>"