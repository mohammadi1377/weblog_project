from fastapi import APIRouter, Depends, HTTPException, status
from ..DataBase.my_database import get_db
from sqlalchemy.orm import Session
from ..schema import CommentSchemaIn, CommentSchema
from .. import oauth2
from ..models import Comment, User, Post
from typing import List

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.post("/", response_model=CommentSchema)
async def create_comment(comment: CommentSchemaIn, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    new_comment = Comment(**comment.dict(), owner_id=current_user.id)

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/accepted/", response_model=List[CommentSchema])
def get_accepted_comments(db: Session = Depends(get_db)):
    db_comment = db.query(Comment).filter(Comment.accepted == True).all()
    return db_comment


def is_super_user_or_owner(db: Session, current_user: User, comment_id: int):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    db_user = db.query(User).filter(User.id == current_user.id).first()
    if db_user.role not in ["superuser", "admin"] and db_comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to perform this action")


@router.get("/{post_id}/", response_model=List[CommentSchema])
async def get_comments(post_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(Comment).filter(Comment.post_id == post_id).all()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


@router.delete("/{comment_id}/")
async def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    is_super_user_or_owner(db, current_user, comment_id)
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(db_comment)
    db.commit()
    return {"detail": "Comment deleted successfully"}


@router.put("/{comment_id}/", response_model=CommentSchema)
async def update_comment(comment_id: int, comment: CommentSchemaIn, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    is_super_user_or_owner(db, current_user, comment_id)

    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Only admin and superuser users can update comments
    if current_user.role not in ["superuser", "admin"]:
        raise HTTPException(status_code=403, detail="You are not authorized to update comments")

    db_comment.text = comment.text
    db.commit()
    db.refresh(db_comment)

    return db_comment

