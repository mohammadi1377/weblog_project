from fastapi import APIRouter, Request, Depends
from .auth import template
from fastapi.responses import HTMLResponse
from ..DataBase.my_database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..models import Post

router = APIRouter(
    tags=["Home"]
)


@router.get("/home/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    last_3_posts = db.query(Post).order_by(desc(Post.created_at)).limit(3)
    return template.TemplateResponse(
        "home.html",
        {"request": request,
         "posts": last_3_posts}
    )


@router.get("/about/", response_class=HTMLResponse)
def about(request: Request):
    return template.TemplateResponse(
        "about.html",
        {"request": request}
    )


@router.get("/contact_us/")
def contact(request: Request):
    return template.TemplateResponse(
        "contact.html",
        {"request": request}
    )


@router.get("/signup/")
def sign_up(request: Request):
    return template.TemplateResponse(
        "signup.html",
        {"request": request}
    )


@router.get("/login/")
def sign_in(request: Request):
    return template.TemplateResponse(
        "login.html",
        {"request": request}
    )
