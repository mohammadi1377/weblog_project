from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text, TIMESTAMP
from .DataBase.my_database import Base
from typing import List


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    user_role = Column(String(20))
    user_name = Column(String(20), unique=True)
    user_email = Column(String(50), unique=True)
    password = Column(String(20))


class Post(Base):
    __tablename__ = "post"
    post_id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(Integer, ForeignKey("users.user_id"))
    post_url = Column(String(100), unique=True)
    post_title = Column(String(20))
    post_image = Column(String(20))
    post_content = Column(Text)
    # post_date = Column(TIMESTAMP)
    # post_modified = Column(TIMESTAMP)
    # category = relationship("Category", back_populates="post")


class Comment(Base):
    __tablename__ = "comment"
    comment_id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("post.post_id"))
    user_name = Column(String(20))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    user_email = Column(String(50))
    comment_date = Column(String(20))
    comment_text = Column(Text)


class Category(Base):
    __tablename__ = "category"
    category_id = Column(Integer, primary_key=True, index=True)
    category_url = Column(String(100), unique=True)
    category_name = Column(String(20))
    category_summary = Column(Text)
    # post = relationship("Post", back_populates="category")
