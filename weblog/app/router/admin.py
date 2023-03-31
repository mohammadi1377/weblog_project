from fastapi import APIRouter, Depends, HTTPException, Request, status
from .. import oauth2
from ..DataBase.my_database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from ..models import Comment, User, Post
from .post import template
from ..schema import UserSchemaOut, CreateUserSchema
from typing import List

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/", response_class=HTMLResponse)
def admin(request: Request):
    # if current_user.role != 'admin':
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    return template.TemplateResponse(
        "admin.html",
        {"request": request},
    )


@router.get("/users/")
def users(request: Request, db: Session = Depends(get_db)):
    db_users = db.query(User).all()
    num = len(db_users)
    return template.TemplateResponse(
        "admin_users.html",
        {"request": request,
         "users": db_users
         }
    )


@router.get("/", response_model=List[UserSchemaOut])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/{id}", response_model=UserSchemaOut)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found.")
    return user


@router.get("/posts/")
def comments(request: Request, db: Session = Depends(get_db)):
    db_posts = db.query(Post).all()
    num = len(db_posts)
    return template.TemplateResponse(
        "admin_posts.html",
        {"request": request,
         "posts": db_posts
         }
    )


@router.get("/unconfirmed_comments/")
def comments(request: Request, db: Session = Depends(get_db)):
    db_comments = db.query(Comment).filter(Comment.accepted == "False").all()
    num = len(db_comments)

    return template.TemplateResponse(
        "unconfirmed_comments.html",
        {"request": request,
         "comments": db_comments
         }
    )


@router.patch("/{id}", response_model=UserSchemaOut, status_code=200)
async def update(user_id: int, user: CreateUserSchema, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    update_user = db.query(User).get(user_id)
    if current_user.role == "admin":
        if update_user.role == "user":
            update_user.role = "superuser"

        elif update_user.role == "superuser":
            update_user.role = "user"

    db.commit()
    db.refresh(update_user)
    return update_user
