from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional


class UserSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

    class Config:
        orm_mode = True


class CreateUserSchema(UserSchema):
    name: str
    confirm_pass: str = Field(min_length=8)

    @validator('confirm_pass')
    @classmethod
    def check_password_confirmation(cls, value, values):
        if values["password"] != value:
            raise ValueError('Password Confirmation must match password')
        return value

    class Config:
        orm_mode = True


class UserSchemaOut(BaseModel):
    # id: int
    role: str
    name: str
    email: EmailStr


    class Config:
        orm_mode = True


class PostSchema(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True


class CommentSchema(BaseModel):
    text: str

    class Config:
        orm_mode = True


class CommentSchemaIn(BaseModel):
    post_id: int
    # owner_id: int
    text: str

    class Config:
        orm_mode = True



class PostSchemaOut(PostSchema):
    post_comments: list[CommentSchema] = []

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[str]
    username: Optional[str]


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# class ConnectionConfig(BaseModel):
#     MAIL_SERVER: str
#     MAIL_PORT: int
#     MAIL_USERNAME: str
#     MAIL_PASSWORD: str
#     MAIL_STARTTLS: bool
#     MAIL_SSL_TLS: bool

