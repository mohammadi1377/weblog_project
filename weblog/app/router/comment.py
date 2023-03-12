from fastapi import APIRouter, Depends, HTTPException, status
from ..DataBase.my_database import get_db
from sqlalchemy.orm import Session
from ..schema import CommentSchema_in, 	CommentSchema_out
from ..modules import Comment, User

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

@router.post("/", response_model=CommentSchema_out)
async def create_comment(comment: CommentSchema_in, db: Session = Depends(get_db)):
	comment_user_name = db.query(User).filter(Comment.user_id == User.user_id).scaler()
	new_comment = Comment(**comment.dict(), user_name=comment_user_name)
	db.add(new_comment)
	db.commit()
	db.refresh(new_comment)
	return new_comment

@router.get("/{comment_id}/", response_model=list[CommentSchema_out])
async def read_comments(post_id: int, db: Session = Depends(get_db)):
	db_comment = db.query(Comment).filter(Comment.post_id == post_id).all()
	if db_comment is None:
		raise HTTPException(status_code=404, detail="Comment not found")
	return db_comment
