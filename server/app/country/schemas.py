from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CountryBase(BaseModel):
    title: str = ''
    description: str = ''
    text: str = ''

    class Config:
        orm_mode = True


class CountryList(CountryBase):
    id: Optional[int]


class CountrySingle(CountryBase):
    pass


class CountryUpdate(CountryBase):
    date: Optional[datetime]


class CountryCreate(CountryBase):
    pass
