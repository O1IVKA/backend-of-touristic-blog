from typing import Optional, List
from fastapi_users import models

from app.city.schemas import CitySingle


class User(models.BaseUser):
    image: Optional[str] = None
    full_name: str = None


class UserCreate(models.BaseUserCreate):
    city_id: int


class UserUpdate(User, models.BaseUserUpdate):
    city_id: int


class UserDB(User, models.BaseUserDB):
    city_id: int


class UserSingle(User):
    city: CitySingle = None
    count_followers: int = None
    count_following: int = None
    class Config:
        orm_mode = True