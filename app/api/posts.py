from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.db import get_db
from app.schemas.post import PostCreateRequest, PostUpdateRequest, PostResponse
from app.services.post_service import PostService

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostResponse)
def create_post(
    data: PostCreateRequest,
    db: Session = Depends(get_db),
):
    return PostService.create_post(db, data)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    return PostService.get_post(db, post_id)


@router.get("/", response_model=List[PostResponse])
def list_posts(
    db: Session = Depends(get_db),
):
    return PostService.get_posts(db)


@router.patch("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    data: PostUpdateRequest,
    db: Session = Depends(get_db),
):
    return PostService.update_post(db, post_id, data)


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
):
    return PostService.delete_post(db, post_id)
