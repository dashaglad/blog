from fastapi import HTTPException
from app.repositories.post_repository import PostRepository
from app.core.config import settings
from app.schemas.post import PostCreateRequest, PostResponse, PostUpdateRequest
from app.utils.cache import Cache
from typing import Any


class PostService:

    @staticmethod
    def _cache_key(post_id: int) -> str:
        return f"post:{post_id}"

    @staticmethod
    def get_post(db, post_id: int) -> PostResponse:
        key = PostService._cache_key(post_id)

        cached = Cache.get(key)
        if cached is not None:
            return PostResponse.model_validate(cached)

        post = PostRepository.get_by_id(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        data: dict[str, Any] = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "created_at": post.created_at.isoformat() if post.created_at else None,
            "updated_at": post.updated_at.isoformat() if post.updated_at else None,
        }

        Cache.set(key, data, ttl=settings.CACHE_TTL)

        return PostResponse.model_validate(data)

    @staticmethod
    def get_posts(db) -> list[PostResponse]:
        posts = PostRepository.get_all(db)

        return [PostResponse.model_validate(post) for post in posts]

    @staticmethod
    def create_post(db, data: PostCreateRequest) -> PostResponse:
        post = PostRepository.create(db, data.model_dump())
        db.commit()
        db.refresh(post)
        return PostResponse.model_validate(post)

    @staticmethod
    def update_post(db, post_id: int, update_data: PostUpdateRequest) -> PostResponse:
        post = PostRepository.get_by_id(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        post = PostRepository.update(
            db,
            post,
            update_data.model_dump(exclude_unset=True),
        )

        db.commit()
        db.refresh(post)

        Cache.delete(PostService._cache_key(post_id))

        return PostResponse.model_validate(post)

    @staticmethod
    def delete_post(db, post_id: int) -> dict[str, bool]:
        post = PostRepository.get_by_id(db, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")

        PostRepository.delete(db, post)

        db.commit()

        Cache.delete(PostService._cache_key(post_id))

        return {"ok": True}
