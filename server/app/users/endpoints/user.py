from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy.orm import Session
from fastapi import UploadFile, File, APIRouter, Depends, HTTPException

from core.config import MEDIA_PATH
from app.users.services import fastapi_users
from app.users import models, services, schemas
from core.db import get_db

router = APIRouter()


@router.put("/update-img/me")
async def update_image_me(
        *,
        db: Session = Depends(get_db),
        image: UploadFile = File(...),
        current_user: models.UserTable = Depends(fastapi_users.get_current_active_user)
):
    """
    User updates his own image
    """
    if image.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")

    file_path = services.generate_unique_img_name(image)
    services.save_image_in_db(db=db, user_id=current_user.id, file_path=file_path)
    services.save_image_in_folder(image=image, file_path=file_path)

    return {
        "id": current_user.id,
        "filename": image.filename
    }


@router.put("/update-img/{id}", dependencies=[Depends(fastapi_users.get_current_user)])
async def update_image_user(
        *,
        id: UUID4,
        db: Session = Depends(get_db),
        image: UploadFile = File(...),
):
    """
    Superuser updates another user's image
    """
    if image.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")

    file_name = services.generate_unique_img_name(image=image)
    file_path = MEDIA_PATH + file_name

    services.save_image_in_db(db=db, user_id=id, file_path=file_path)
    services.save_image_in_folder(image=image, file_path=file_path)
    return {
        "id": id,
        "filename": file_name
    }


@router.post("/follow/{id}")
def follow_user(
        *,
        id: UUID4,
        db: Session = Depends(get_db),
        current_user: models.UserTable = Depends(fastapi_users.get_current_active_user)
):
    services.follow(key="follow", db=db, user_id=id, current_user_id=current_user.id)
    return {"follow": "Ok"}


@router.post("/unfollow/{id}")
def unfollow_user(
        *,
        id: UUID4,
        db: Session = Depends(get_db),
        current_user: models.UserTable = Depends(fastapi_users.get_current_active_user)
):
    services.follow(key="unfollow", db=db, user_id=id, current_user_id=current_user.id)
    return {"unfollow": "Ok"}


@router.get("/{id}", response_model=schemas.UserSingle)
def get_user(id: UUID4, db: Session = Depends(get_db)):
    user = services.get_user(user_id=id, db=db)
    extend_user = services.extend_count_follow_fields(user=user)
    return extend_user
