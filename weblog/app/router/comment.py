from fastapi import APIRouter, Depends, HTTPException
from ..DataBase.my_database import get_db
from sqlalchemy.orm import Session
from ..schema import CommentSchemaIn, CommentSchemaOut
from ..models import Comment, User
from .. import oauth2

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)


@router.post("/", response_model=CommentSchemaOut)
async def create_comment(comment: CommentSchemaIn, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    new_comment = Comment(**comment.dict(), owner=current_user)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/{comment_id}/", response_model=list[CommentSchemaOut])
async def get_comments(post_id: int, db: Session = Depends(get_db)):
    db_comment = db.query(Comment).filter(Comment.post_id == post_id).all()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment
