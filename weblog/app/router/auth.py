from fastapi import APIRouter, Depends, HTTPException, status, Response,Request
from ..DataBase.my_database import get_db
from sqlalchemy.orm import Session
from ..schema import UserSchema, UserSchemaOut, Token
from ..modules import User
from app.utils import verify
from ..oauth2 import create_access_token

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)


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
    user = db.query(User).filter(User.user_email == user_instance.user_email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not verify(user_instance.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    access_token = create_access_token(data={"user_id": user.user_id, "sub": user.user_email})
    return Token(access_token=access_token)
