from fastapi import APIRouter, Depends, HTTPException, status
from .. import oauth2
from ..DataBase.my_database import get_db
from sqlalchemy.orm import Session
from ..schema import PostSchema, PostSchemaOut
from ..models import Post, User
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/{post_id}", response_model=PostSchemaOut, status_code=200)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).get(post_id)

    check_if_exists(db_post, post_id)
    return db_post


@router.get("/", response_model=List[PostSchemaOut], status_code=200)
async def get_posts(db: Session = Depends(get_db)):
    db_posts = db.query(Post).all()
    return db_posts


@router.post("/", response_model=PostSchemaOut, status_code=200)
async def create_post(post: PostSchema, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    new_post = Post(**post.dict(), owner=current_user)
    db.add(new_post)
    db.commit()
    return new_post


@router.patch("/{post_id}", response_model=PostSchema, status_code=200)
async def update(post_id: int, post: PostSchema, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    update_post = db.query(Post).get(post_id)

    check_if_exists(update_post, post_id)
    if update_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    update_post.title = post.title
    update_post.content = post.content
    update_post.image = post.image

    db.commit()
    db.refresh(update_post)
    return update_post


@router.delete('/{post_id}', status_code=200)
async def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    db_delete = db.query(Post).get(post_id)
    if db_delete.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    if not db_delete:
        raise HTTPException(status_code=204, detail=f"Post {post_id} does not exist")
    db.delete(db_delete)
    db.commit()
    return None


def check_if_exists(post, post_id):
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id:{post_id} was not found")
