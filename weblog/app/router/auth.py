from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.templating import Jinja2Templates
from ..DataBase.my_database import get_db
from sqlalchemy.orm import Session
from ..schema import UserSchema, UserSchemaOut, Token
from ..models import User
from app.utils import verify
from ..oauth2 import create_access_token

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

template = Jinja2Templates(directory="Template")


@router.get("/login")
def login(request: Request):
    return template.TemplateResponse(
        "login.html",
        {"request": request}
    )


@router.get("/logout")
def logout(response: Response):
    response.delete_cookie("token")
    # settings.user_login = None
    return {"status": "Logout successful"}


@router.post("/login", response_model=UserSchemaOut)
def login(user_instance: UserSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_instance.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not verify(user_instance.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = create_access_token(data={"user_id": user.id, "sub": user.email})
    return Token(access_token=access_token)
