from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserSchema(BaseModel):
    user_email: EmailStr
    password: str = Field(unique=True, min_length=8)

    class Config:
        orm_mode = True


class CreateUserSchema(UserSchema):
    user_name: str = Field(unique=True)

    class Config:
        orm_mode = True


class UserSchemaOut(BaseModel):
    user_id: int
    user_role: str = "User"
    user_name: str = Field(unique=True)
    user_email: EmailStr

    class Config:
        orm_mode = True


class CommentSchema(BaseModel):
    post_id: int = Field(unique=True)
    user_name: str = Field(unique=True)
    user_id: int = Field(unique=True)
    user_email: EmailStr
    comment_date: str
    comment_text: str

    class Config:
        orm_mode = True


class PostSchema(BaseModel):
    post_title: str
    post_image: str
    post_content: str

    class Config:
        orm_mode = True


class PostSchemaOut(PostSchema):
    post_comments: list[CommentSchema] | None

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[str]
    username: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

