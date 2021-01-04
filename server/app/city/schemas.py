from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.country.schemas import CountrySingle


class CityBase(BaseModel):
    title: str = ''
    description: str = ''
    text: str = ''
    country_id: int

    class Config:
        orm_mode = True


class CityList(CityBase):
    id: Optional[int]


class CitySingle(CityBase):
    country: CountrySingle


class CityUpdate(CityBase):
    date: Optional[datetime]


class CityCreate(CityBase):
    pass
