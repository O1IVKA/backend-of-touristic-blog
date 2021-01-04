import re
import shutil
import uuid

from fastapi import File, UploadFile, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.orm import Session

from app.users import schemas
from app.users.models import UserTable, user_to_user
from core.config import SECRET
from core.db import database

users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(schemas.UserDB, database, users)

jwt_authentication = JWTAuthentication(
    secret=SECRET, lifetime_seconds=3600, tokenUrl="/auth/jwt/login"
)

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    schemas.User,
    schemas.UserCreate,
    schemas.UserUpdate,
    schemas.UserDB,
)


def generate_unique_img_name(image: UploadFile = File(...)):
    name, ext = re.split("\.", image.filename)
    file_name = name + f'_{uuid.uuid4().hex}.{ext}'
    return file_name


def save_image_in_db(db: Session, file_path: str, user_id: UUID4):
    user = db.query(UserTable).filter(UserTable.id == user_id).first()
    user.image = file_path
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def save_image_in_folder(file_path: str, image: UploadFile = File(...)):
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)


def get_user(db: Session, user_id: UUID4):
    user = db.query(UserTable).filter(UserTable.id == user_id).first()
    return user


def follow(key: str, db: Session, user_id: UUID4, current_user_id: UUID4):
    follower_user = get_user(db=db, user_id=current_user_id)
    followed_user = get_user(db=db, user_id=user_id)

    if key == "follow":
        follower_user.following.append(followed_user)
    elif key == "unfollow":
        follower_user.following.remove(followed_user)

    db.add(follower_user)
    db.commit()
    db.refresh(follower_user)
    return follower_user


def extend_count_follow_fields(user: UserTable):
    """
    Add field count_followers and count_following to user object
    DB table UserTable does not have this fields!
    """
    setattr(user, 'count_followers', len(user.followers))
    setattr(user, 'count_following', len(user.following))
    user = jsonable_encoder(user)
    return user
