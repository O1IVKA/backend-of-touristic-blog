from fastapi_users.db.sqlalchemy import GUID
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, sql
from sqlalchemy.orm import relationship, backref
from core.db import Base


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String)
    description = Column(String(350))
    text = Column(String(350))
    country_id = Column(Integer, ForeignKey('country.id'))
    country = relationship("Country",  backref="city")

cities = City.__table__