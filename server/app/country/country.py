from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import services, schemas
from ..users.models import UserTable
from ..users.services import fastapi_users
from core.db import get_db

router = APIRouter()

@router.get("/{country_id}", response_model=schemas.CountrySingle)
def get_country(*, country_id, db: Session = Depends(get_db)):
    country = services.crud_country.get(db=db, id=country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    return country


@router.get("/", response_model=List[schemas.CountrySingle])
def get_list_countries(*, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    countries = services.crud_country.get_multi(skip=skip, limit=limit, db=db)
    if not countries:
        raise HTTPException(status_code=404, detail="Country not found")
    return countries


@router.post("/create", response_model=schemas.CountryCreate)
def create_country(
        *,
        db: Session = Depends(get_db),
        country_in: schemas.CountryCreate,
        current_user: UserTable = Depends(fastapi_users.get_current_active_user),
):
    if not current_user:
        raise HTTPException(status_code=403, detail="Unauthorized")
    country = services.crud_country.create(db=db, obj_in=country_in)
    return country


@router.put("/update/{id}", response_model=schemas.CountryUpdate)
def update_post(
        *,
        db: Session = Depends(get_db),
        id: int,
        country_in: schemas.CountryUpdate,
        current_user: UserTable = Depends(fastapi_users.get_current_active_user),
):
    country = services.crud_country.get(db=db, id=id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    country = services.crud_country.update(db=db, db_obj=country, obj_in=country_in)
    return country


@router.delete("/delete/{id}", response_model=schemas.CountrySingle)
async def delete_country(
        *,
        db: Session = Depends(get_db),
        id: int,
        current_user: UserTable = Depends(fastapi_users.get_current_active_user),
):
    country = services.crud_country.get(db=db, id=id)
    if not country:
        raise HTTPException(status_code=404, detail="Post not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=404, detail="Not enough permissions")
    country = services.crud_country.remove(db=db, id=id)
    return country