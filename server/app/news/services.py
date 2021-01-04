import shutil
import uuid
import re
from fastapi import HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.params import File
from pydantic import UUID4
from slugify import slugify
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.news import schemas
from .models import PostLike, Tag, Post, Comment
from app.base.crud import CRUDBase
from ..city.models import City
from ..users.models import UserTable


class CRUDPost(CRUDBase[Post, schemas.PostCreate, schemas.PostUpdate]):
    """CRUD for Post"""

    def create_with_owner_and_tags(
            self, db: Session, *, obj_in: schemas.PostCreate, user_id: UUID4
    ) -> Post:
        """Create post with user and tags"""
        tags = db.query(Tag).filter(Tag.id.in_(obj_in.tag)).all()
        slug = generate_slug(obj_in.title)

        obj_in_data = jsonable_encoder(obj_in, exclude={"tag"})
        db_obj = Post(**obj_in_data, user_id=user_id, slug=slug, tag=tags)
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="IntegrityError")
        return db_obj


class CRUDComment(CRUDBase[Comment, schemas.CommentCreate, schemas.CommentUpdate]):
    """CRUD for Comment"""

    def get_without_parent(self, db: Session, id: int):
        return db.query(self.model).filter_by(parent=None).filter(self.model.id == id).first()

    def get_multi_without_parent(self, db: Session, *, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter_by(parent=None).offset(skip).limit(limit).all()


class CRUDTag(CRUDBase[Tag, schemas.TagCreate, schemas.TagUpdate]):
    """CRUD for Post"""
    pass


# create CRUD object for posts
crud_post = CRUDPost(Post)

# create CRUD object for comments
crud_comment = CRUDComment(Comment)

# create CRUD object for tags
crud_tag = CRUDTag(Tag)


def like(db: Session, post_id: int, user_id: UUID4):
    like_post = PostLike(user_id=user_id, post_id=post_id)
    db.add(like_post)
    db.commit()
    db.refresh(like_post)
    return like_post


def unlike(db: Session, post_id: int, user_id: UUID4):
    unlike_post = db.query(PostLike).filter_by(user_id=user_id, post_id=post_id).first()
    db.delete(unlike_post)
    db.commit()
    return unlike_post


def count_likes(db: Session, post_id: int):
    count = db.query(PostLike).filter_by(post_id=post_id).count()
    return count


def has_liked_post(db: Session, post_id: int, user_id: UUID4):
    return db.query(PostLike).filter_by(user_id=user_id, post_id=post_id).count() > 0


def post_filters(db: Session, skip: int = 0, limit: int = 100, search: str = None,
                 tag: list = None,
                 city: str = None):
    list_filters = []
    if search:
        # add filter search by title
        list_filters.append(Post.title.match(search))
        # add filter search by text
        list_filters.append(Post.text.match(search))
    if tag:
        # add filter by tags
        for tag_name in tag:
            list_filters.append(Tag.title == tag_name)
    if city:
        # add filter by city)
        city_obj = db.query(City).filter(City.title == city).first()
        list_filters.append(Post.city == city_obj)

    filtered_posts = db.query(Post) \
        .filter(or_(*list_filters)) \
        .order_by(Post.date.desc()) \
        .offset(skip) \
        .limit(limit) \
        .all()

    return filtered_posts

def generate_unique_img_name(image: UploadFile = File(...)):
    name, ext = re.split("\.", image.filename)
    file_name = name + f'_{uuid.uuid4().hex}.{ext}'
    return file_name


def save_image_in_db(db: Session, file_path: str, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    post.image = file_path
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def save_image_in_folder(file_path: str, image: UploadFile = File(...)):
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

def generate_slug(text: str):
    return slugify(text)
