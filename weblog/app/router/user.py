from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from .. import oauth2
from ..DataBase.my_database import get_db
from sqlalchemy.orm import Session
from ..schema import CreateUserSchema, UserSchemaOut
from ..models import *
from ..utils import hash_password
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

security = HTTPBearer()


@router.post("/regiregister/", status_code=status.HTTP_201_CREATED, response_model=UserSchemaOut)
def create_user(user: CreateUserSchema, db: Session = Depends(get_db)):
    new_user = User(name=user.name,
                    email=user.email,
                    password=hash_password(user.password),
                    )
    db.add(new_user)
    db.commit()

    return new_user


@router.patch("/user/{id}", response_model=UserSchemaOut, status_code=200)
async def update(user_id: int, user: CreateUserSchema, db: Session = Depends(get_db)):
    update_user = db.query(User).get(user_id)

    update_user.name = user.name
    update_user.email = user.email
    update_user.password = hash_password(user.password)

    db.commit()
    db.refresh(update_user)
    return update_user


@router.delete('/user/{id}', status_code=200)
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):

    if current_user.role not in ['admin', 'superuser']:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db_delete = db.query(User).get(user_id)

    if not db_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id:{user_id} was not found")

    # if db_delete.id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db.delete(db_delete)
    db.commit()
    return {"detail": "user deleted successfully"}


def check_if_exists(user, user_id):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {user_id} id was not found")
