from fastapi import APIRouter, Depends, HTTPException
from ..DataBase.my_database import get_db
from sqlalchemy.orm import Session
from ..schema import *
from ..modules import *

router = APIRouter(
    prefix="/v1/posts",
    tags=["Posts"]
)


@router.get("/post/{id}", response_model=PostSchema, status_code=200)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).get(post_id)
    return db_post


@router.get("/posts", response_model=PostSchema, status_code=200)
async def get_posts(db: Session = Depends(get_db)):
    db_posts = db.query(Post).all
    return db_posts


@router.post("/post/", response_model=PostSchema, status_code=200)
async def create_post(post: PostSchema, db: Session = Depends(get_db)):
    new_post = Post(user_id=post.user_id,
                    post_title=post.post_title,
                    post_url=post.post_url,
                    post_content=post.post_content,
                    post_image=post.post_image
                    )

    db.add(create_post)
    db.commit()
    return new_post


@router.patch("/post/{id}", response_model=PostSchema, status_code=200)
async def update(post_id: int, post: PostSchema, db: Session = Depends(get_db)):
    update_post = db.query(Post).get(post_id)

    update_post.post_title = post.post_title
    update_post.post_content = post.post_content
    update_post.post_image = post.post_image
    db.refresh(update_post)
    db.commit()
    return update_post


@router.delete('/post/{id}', status_code=200)
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_delete = db.query(Post).get(post_id)
    if not db_delete:
        raise HTTPException(status_code=404, detail=f"Post {post_id} does not exist")
    db.delete(db_delete)
    db.commit()
    return None
