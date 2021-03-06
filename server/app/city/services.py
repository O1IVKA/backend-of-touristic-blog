from typing import List

from fastapi.encoders import jsonable_encoder
from fastapi_users.db.sqlalchemy import GUID
from sqlalchemy.orm import Session

from . import schemas

from core.db import database
from sqlalchemy import select

from .models import City
from ..users.schemas import User
from ..users.services import users
from ..base.crud import CRUDBase
#
# async def get_post_list():
#     post_list = await database.fetch_all(query=posts.select())
#     return [dict(result) for result in post_list]
#
#
# async def get_post(pk: int):
#     u = users.alias('user')
#     p = posts.alias('post')
#     q = select([u.c.id.label("userId"), u.c.email.label("userName"), p]) \
#         .select_from(p.join(u)) \
#         .where((p.c.id == pk) & (u.c.id == p.c.user))
#     post = await database.fetch_one(q)
#     if post is not None:
#         post = dict(post)
#         return {**post, "user": {"id": post.pop("userId"), "name": post.pop("userName")}}
#     return None
#
#
# async def get_post_list_user(user: User):
#     post_list = await database.fetch_all(query=posts.select().where(posts.c.user == user.id))
#     return [dict(result) for result in post_list]
#
#
# async def create_post(item: PostCreate, user: User):
#     post = posts.insert().values(**item.dict(), user=user.id)
#     pk = await database.execute(post)
#     return {**item.dict(), "id": pk, "user": {"id": user.id}}
#
#
# async def update_post(pk: int, item: PostCreate, user: User):
#     post = posts.update().where((posts.c.id == pk) & (posts.c.user == user.id)).values(
#         **item.dict())
#     return await database.execute(post)
#
#
# async def delete_post(pk: int, user: User):
#     post = posts.delete().where((posts.c.id == pk) & (posts.c.user == user.id))
#     return await database.execute(post)


class CRUDCity(CRUDBase[City, schemas.CityCreate, schemas.CityUpdate]):
    """CRUD for Post"""
    pass

# create CRUD object for posts
crud_city = CRUDCity(City)