from sqlalchemy.orm import Session
from src.database.models import Comment
from src.schemas import CommentCreate

def create_comment(db: Session, comment: CommentCreate, user_id: int):
    db_comment = Comment(
        content=comment.content,
        post_id=comment.post_id,
        user_id=user_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Comment).offset(skip).limit(limit).all()

def get_comment_by_id(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()

def update_comment(db: Session, comment_id: int, content: str):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment:
        db_comment.content = content
        db.commit()
        db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
    return db_comment

def block_comment(db: Session, comment_id: int):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment:
        db_comment.is_blocked = True
        db.commit()
        db.refresh(db_comment)
    return db_comment
