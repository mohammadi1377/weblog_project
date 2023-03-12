from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text, TIMESTAMP
from .DataBase.my_database import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    user_role = Column(String(20))
    user_name = Column(String(20), unique=True)
    user_email = Column(String(50), unique=True)
    password = Column(String(20))
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")



class Post(Base):
    __tablename__ = "post"
    post_id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(Integer, ForeignKey("users.user_id"))
    post_url = Column(String(100), unique=True)
    post_title = Column(String(20))
    post_image = Column(String(20))
    post_content = Column(Text)
    post_date = Column(TIMESTAMP)
    post_modified = Column(TIMESTAMP)
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")


class Comment(Base):
    __tablename__ = "comment"
    comment_id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("post.post_id"))
    user_name = Column(String(20))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    comment_date = Column(TIMESTAMP)
    comment_text = Column(Text)
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")


