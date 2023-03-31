from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text, Boolean
from .DataBase.my_database import Base
from datetime import date


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(20), default="user")
    name = Column(String(20), unique=True)
    email = Column(String(50), unique=True)
    password = Column(Text)
    created_at = Column(Date, default=date.today())


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(ForeignKey("users.id"))
    owner = relationship("User", backref="posts")
    title = Column(String(20))
    content = Column(Text)
    created_at = Column(Date, default=date.today())
    modified_at = Column(Date, default=date.today())


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(ForeignKey("posts.id"))
    post = relationship("Post", backref="comments")
    owner_id = Column(ForeignKey("users.id"))
    owner = relationship("User", backref="comments")
    text = Column(String(200))
    created_at = Column(Date, default=date.today())
    accepted = Column(Boolean, nullable=False, server_default='False')
