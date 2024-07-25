from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from src.database.db import get_db
from src.schemas import CommentCreate, CommentResponse
from src.services.comments import create_new_comment, handle_blocking
from src.repository.comments import get_comments, get_comment_by_id, update_comment, delete_comment
from src.database.models import Comment
from src.routes.auth import get_current_user

router = APIRouter(prefix="/api/comments", tags=['comments'])

@router.post("/comments/", response_model=CommentResponse)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return create_new_comment(db, comment, user_id)

@router.get("/comments/", response_model=List[CommentResponse])
def read_comments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_comments(db, skip=skip, limit=limit)

@router.get("/comments/{comment_id}", response_model=CommentResponse)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = get_comment_by_id(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@router.put("/comments/{comment_id}", response_model=CommentResponse)
def update_comment_content(comment_id: int, content: str, db: Session = Depends(get_db)):
    db_comment = update_comment(db, comment_id, content)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@router.delete("/comments/{comment_id}", response_model=CommentResponse)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = delete_comment(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@router.post("/comments/block/{comment_id}", response_model=CommentResponse)
def block_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = handle_blocking(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@router.get("/comments-daily-breakdown")
def get_comments_daily_breakdown(date_from: str, date_to: str, db: Session = Depends(get_db)):
    query = db.query(
        func.date(Comment.created_at).label("date"),
        func.count(Comment.id).label("total_comments"),
        func.sum(case([(Comment.is_blocked == True, 1)], else_=0)).label("blocked_comments")
    ).filter(
        Comment.created_at >= date_from,
        Comment.created_at <= date_to
    ).group_by(
        func.date(Comment.created_at)
    ).all()
    
    return [{"date": r.date, "total_comments": r.total_comments, "blocked_comments": r.blocked_comments} for r in query]
