from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, services
from app.users.models import UserTable
from app.users.services import fastapi_users
from core.db import get_db

router = APIRouter()


@router.get("/{tag_id}", response_model=schemas.TagSingle)
def get_tag(*, tag_id: int, db: Session = Depends(get_db)):
    tag = services.crud_tag.get(db=db, id=tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.get("/", response_model=List[schemas.TagSingle])
def get_list_tag(*, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tag = services.crud_tag.get_multi(skip=skip, limit=limit, db=db)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.post("/", response_model=schemas.TagCreate,
             dependencies=[Depends(fastapi_users.get_current_superuser)])
def create_tag(
        *,
        db: Session = Depends(get_db),
        tag_in: schemas.TagCreate,
):
    tag = services.crud_tag.create(db=db, obj_in=tag_in)
    return tag


@router.put("/{id}", response_model=schemas.TagUpdate,
            dependencies=[Depends(fastapi_users.get_current_superuser)])
def update_tag(
        *,
        db: Session = Depends(get_db),
        id: int,
        tag_in: schemas.TagUpdate,
):
    tag = services.crud_tag.get(db=db, id=id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag = services.crud_tag.update(db=db, db_obj=tag, obj_in=tag_in)
    return tag


@router.delete("/{id}", response_model=schemas.TagSingle,
               dependencies=[Depends(fastapi_users.get_current_superuser)])
async def delete_tag(
        *,
        db: Session = Depends(get_db),
        id: int,
):
    tag = services.crud_tag.get(db=db, id=id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag = services.crud_tag.remove(db=db, id=id)
    return tag
