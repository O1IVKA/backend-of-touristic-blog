from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.news import services, schemas, models
from app.users.models import UserTable
from app.users.services import fastapi_users
from core.db import get_db

router = APIRouter()


@router.get("/{id}", response_model=schemas.CommentSingle)
def get_comment(*, db: Session = Depends(get_db), id: int):
    comment = services.crud_comment.get_without_parent(db=db, id=id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.get("/", response_model=List[schemas.CommentSingle])
def get_list_comments(*, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = services.crud_comment.get_multi_without_parent(skip=skip, limit=limit, db=db)
    if not comments:
        raise HTTPException(status_code=404, detail="Comments not found")
    return comments


@router.post("/{post_id}", response_model=schemas.CommentCreate)
def create_comment(
        *,
        post_id: int,
        comment_in: schemas.CommentCreate,
        db: Session = Depends(get_db),
        current_user: UserTable = Depends(fastapi_users.get_current_active_user),
):
    obj_comment = models.Comment(**comment_in.dict(), post_id=post_id, user_id=current_user.id)
    comment = services.crud_comment.create(db=db, obj_in=obj_comment)
    return comment


@router.post("/{post_id}/{comment_id}", response_model=schemas.CommentSingle)
def create_comment_reply(
        *,
        post_id: int,
        comment_id: int,
        comment_in: schemas.CommentCreate,
        db: Session = Depends(get_db),
        current_user: UserTable = Depends(fastapi_users.get_current_active_user),
):
    obj_comment = models.Comment(**comment_in.dict(), post_id=post_id, parent_id=comment_id,
                                 user_id=current_user.id)
    comment = services.crud_comment.create(db=db, obj_in=obj_comment)
    return comment


@router.put("/{id}", response_model=schemas.CommentUpdate)
def update_comment(
        *,
        id: int,
        comment_in: schemas.CommentUpdate,
        db: Session = Depends(get_db),
        current_user: UserTable = Depends(fastapi_users.get_current_active_user),
):
    comment = services.crud_comment.get(db=db, id=id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if not current_user.is_superuser and (comment.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    comment = services.crud_comment.update(db=db, db_obj=comment, obj_in=comment_in)
    return comment


@router.delete("/{id}", response_model=schemas.CommentSingle)
def delete_comment(
        *,
        id: int,
        db: Session = Depends(get_db),
        current_user: UserTable = Depends(fastapi_users.get_current_active_user),
):
    comment = services.crud_comment.get(db=db, id=id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if not current_user.is_superuser and (comment.user_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    comment = services.crud_comment.remove(db=db, id=id)
    return comment
