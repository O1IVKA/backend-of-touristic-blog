import uuid

from fastapi_users.db.sqlalchemy import GUID
from pydantic import BaseModel, UUID4, validator
from typing import Optional, List
from datetime import datetime
from app.city.schemas import CitySingle
from app.users.schemas import UserSingle, User
forbidden_words = ["fuck"]


class Like(BaseModel):
    """Base model schemas like"""
    id: int
    user_id: UUID4
    post_id: int

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    """Base model schemas comment"""
    text: str

    class Config:
        orm_mode = True
    @validator('text')
    def text_validation(cls, v):
        for i in forbidden_words:
            if i in  v:
                raise ValueError('mustn`t contain forbidden words')
            return v.title()


class CommentSingle(CommentBase):
    id: int
    parent_id: Optional[int] = None
    post_id: int
    replies: List['CommentSingle'] = []


CommentSingle.update_forward_refs()


class CommentCreate(CommentBase):
    pass
class CommentUpdate(CommentBase):
    pass


class TagBase(BaseModel):
    """Base model schemas post"""
    title: str = ''

    class Config:
        orm_mode = True


class TagSingle(TagBase):
    id: Optional[int]


class TagUpdate(TagBase):
    pass


class TagCreate(TagBase):
    pass


class PostBase(BaseModel):
    """Base model schemas post"""
    title: str = ''
    text: str = ''
    city_id: int
    image: Optional[str] = None
    class Config:
        orm_mode = True


class PostSingle(PostBase):
    id: Optional[int]
    city: CitySingle = None
    date: Optional[datetime]
    tag: List[TagSingle] = []
    comment: List[CommentSingle] = []
    user_id:UUID4
    user: UserSingle = None

    class Config:
        orm_mode = True

class PostUpdate(PostBase):
    pass


class PostCreate(PostBase):
    tag: List[int] = None



