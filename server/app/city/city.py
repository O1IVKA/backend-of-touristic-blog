from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import services, schemas
from ..users.models import UserTable
from ..users.services import fastapi_users
from core.db import get_db

router = APIRouter()

@router.get("/{city_id}", response_model=schemas.CitySingle)
def get_city(*, city_id, db: Session = Depends(get_db)):
    city = services.crud_city.get(db=db, id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="Country not found")
    return city


@router.get("/", response_model=List[schemas.CitySingle])
def get_list_cities(*, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = services.crud_city.get_multi(skip=skip, limit=limit, db=db)
    if not cities:
        raise HTTPException(status_code=404, detail="Country not found")
    return cities


@router.post("/create", response_model=schemas.CityCreate)
def create_city(
        *,
        db: Session = Depends(get_db),
        city_in: schemas.CityCreate,
        current_user: UserTable = Depends(fastapi_users.get_current_active_user),
):
    if not current_user:
        raise HTTPException(status_code=403, detail="Unauthorized")
    city = services.crud_city.create(db=db, obj_in=city_in)
    return city


@router.put("/update/{id}", response_model=schemas.CityUpdate)
def update_city(
        *,
        db: Session = Depends(get_db),
        id: int,
        city_in: schemas.CityUpdate,
        current_user: UserTable = Depends(fastapi_users.get_current_active_user),
):
    city = services.crud_city.get(db=db, id=id)
    if not city:
        raise HTTPException(status_code=404, detail="Country not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    city = services.crud_city.update(db=db, db_obj=city, obj_in=city_in)
    return city


@router.delete("/delete/{id}", response_model=schemas.CitySingle)
async def delete_city(
        *,
        db: Session = Depends(get_db),
        id: int,
        current_user: UserTable = Depends(fastapi_users.get_current_active_user),
):
    city = services.crud_city.get(db=db, id=id)
    if not city:
        raise HTTPException(status_code=404, detail="Post not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=404, detail="Not enough permissions")
    city = services.crud_city.remove(db=db, id=id)
    return city