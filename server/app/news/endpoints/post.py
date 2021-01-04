from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from fastapi.params import File
from pydantic.types import UUID4
from sqlalchemy.orm import Session

from app.news import services, schemas
from app.users.models import UserTable
from app.users.services import fastapi_users, get_user
from core.config import MEDIA_PATH
from core.db import get_db

router = APIRouter()


class FilterQueryParams:
    def __init__(self,
                 search: Optional[str] = None,
                 skip: int = 0,
                 limit: int = 100,
                 tag: Optional[List[str]] = Query(None),
                 # city: Optional[List[str]] = Query(None),
                 city: Optional[str] = None,
                 ):

        self.search = search
        self.skip = skip
        self.limit = limit
        self.tag = tag
        self.city = city


@router.get("/{slug}", response_model=schemas.PostSingle)
def get_post(*, slug: str, db: Session = Depends(get_db)):
    post = services.crud_post.get_by_slug(db=db, slug=slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/", response_model=List[schemas.PostSingle])
def get_list_posts(db: Session = Depends(get_db), common: FilterQueryParams = Depends()):
    posts = services.post_filters(db=db, skip=common.skip, limit=common.limit, search=common.search,
                                  tag=common.tag,
                                  city=common.city)
    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found")
    return posts


@router.post("/", response_model=schemas.PostSingle)
def create_post(
        *,
        db: Session = Depends(get_db),
        post_in: schemas.PostCreate,
        current_user: UserTable = Depends(fastapi_users.get_current_active_user),
) -> Any:
    post = services.crud_post.create_with_owner_and_tags(db=db, obj_in=post_in, user_id=current_user.id)
    return post


@router.put("/{id}", response_model=schemas.PostUpdate)
def update_post(
        *,
        db: Session = Depends(get_db),
        id: int,
        post_in: schemas.PostUpdate,
        current_user: UserTable = Depends(fastapi_users.get_current_active_user),
):
    post = services.crud_post.get(db=db, id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if not current_user.is_superuser and (post.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    post = services.crud_post.update(db=db, db_obj=post, obj_in=post_in)
    return post


@router.delete("/{id}", response_model=schemas.PostBase)
async def delete_post(
        *,
        db: Session = Depends(get_db),
        id: int,
        current_user: UserTable = Depends(fastapi_users.get_current_active_user),
):
    post = services.crud_post.get(db=db, id=id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if not current_user.is_superuser and (post.user_id != current_user.id):
        raise HTTPException(status_code=404, detail="Not enough permissions")
    post = services.crud_post.remove(db=db, id=id)
    return post

@router.put("/update-img/{id}", dependencies=[Depends(fastapi_users.get_current_user)])
async def update_image_post(
        *,
        id: int,
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

    services.save_image_in_db(db=db, post_id=id, file_path=file_path)
    services.save_image_in_folder(image=image, file_path=file_path)
    return {
        "id": id,
        "filename": image.filename
    }

