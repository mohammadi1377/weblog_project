from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text, TIMESTAMP
from .DataBase.my_database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(20))
    name = Column(String(20), unique=True)
    email = Column(String(50), unique=True)
    password = Column(String(20))
    posts = relationship("Post", back_populates="owner")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(ForeignKey("users.id"))
    owner = relationship("User", back_populates="posts")
    title = Column(String(20))
    # image = Column(BLOB)
    content = Column(Text)
    # created_at = Column(TIMESTAMP, nullable=True)
    # modified_at = Column(TIMESTAMP, nullable=True)
    # comments_id = Column(ForeignKey("comments.id"))
    comments = relationship("Comment", back_populates="posts")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(ForeignKey("posts.id"))
    owner_id = Column(ForeignKey("users.id"))
    # date = Column(TIMESTAMP)
    text = Column(Text)
    owner = relationship("User")
    post = relationship("Post")
