from fastapi import APIRouter, Depends, HTTPException, status
from ..DataBase.my_database import get_db
from sqlalchemy.orm import Session
from ..schema import CreateUserSchema, UserSchemaOut
from ..models import *
from ..utils import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=UserSchemaOut)
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get("/{user_id}", response_model=UserSchemaOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    check_if_exists(user, user_id)
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserSchemaOut)
def create_user(user: CreateUserSchema, db: Session = Depends(get_db)):
    new_user = User(user_name=user.user_name,
                    user_email=user.user_email,
                    password=hash_password(user.password))
    db.add(new_user)
    db.commit()

    return new_user


@router.patch("/user/{id}", response_model=UserSchemaOut, status_code=200)
async def update(user_id: int, user: CreateUserSchema, db: Session = Depends(get_db)):
    update_user = db.query(User).get(user_id)

    update_user.user_name = user.user_name
    update_user.user_email = user.user_email
    update_user.password = hash_password(user.password)

    db.commit()
    db.refresh(update_user)
    return update_user


@router.delete('/user/{id}', status_code=200)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_delete = db.query(User).get(user_id)
    if not db_delete:
        raise HTTPException(status_code=404, detail=f"Post {user_id} does not exist")
    db.delete(db_delete)
    db.commit()
    return None


def check_if_exists(user, user_id):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {user_id} id was not found")
