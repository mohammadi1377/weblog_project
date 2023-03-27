from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserSchema(BaseModel):
    email: EmailStr
    password: str = Field(unique=True, min_length=8)

    class Config:
        orm_mode = True


class CreateUserSchema(UserSchema):
    name: str = Field(unique=True)

    class Config:
        orm_mode = True


class UserSchemaOut(BaseModel):
    id: int
    role: str
    name: str #= Field(unique=True)
    email: EmailStr

    class Config:
        orm_mode = True


class PostSchema(BaseModel):
    title: str
    # image: bytes
    content: str
    #owner: UserSchemaOut

    class Config:
        orm_mode = True


class CommentSchema(BaseModel):
    # post: PostSchemaOut
    # owner: UserSchemaOut
    text: str


class CommentSchemaIn(BaseModel):
    post_id: int = Field(unique=True)
    comment_text: str

    class Config:
        orm_mode = True


class CommentSchemaOut(CommentSchema):
    text: str
    owner: UserSchemaOut

    class Config:
        orm_mode = True


class CommentSchemaRef(CommentSchemaOut):
    post: PostSchema
    owner: UserSchemaOut


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
