from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserSchema(BaseModel):
    user_role: str
    user_name: str = Field(unique=True)
    user_email: EmailStr
    password: str = Field(unique=True, min_length=8)

    class Config:
        orm_mode = True


class PostSchema(BaseModel):
    post_url: str
    post_title: str
    post_image: str
    post_content: str
    # post_date: datetime
    # post_modified: datetime

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


class CategorySchema(BaseModel):
    category_url: str = Field(unique=True)
    category_name: str
    category_summary: str

    class Config:
        orm_mode = True
