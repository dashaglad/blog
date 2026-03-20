from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.post import Post


class PostRepository:

    @staticmethod
    def create(db: Session, data):
        post = Post(**data)
        db.add(post)
        db.flush()
        return post

    @staticmethod
    def get_by_id(db: Session, post_id: int):
        return db.query(Post).filter(Post.id == post_id).first()

    @staticmethod
    def update(db: Session, post: Post, data: dict):
        for key, value in data.items():
            setattr(post, key, value)
        db.flush()
        return post

    @staticmethod
    def delete(db: Session, post: Post):
        db.delete(post)
        db.flush()

    @staticmethod
    def get_all(db: Session):
        return db.query(Post).order_by(Post.created_at).all()
