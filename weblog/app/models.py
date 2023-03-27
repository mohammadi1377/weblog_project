from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text, TIMESTAMP
from .DataBase.my_database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(20), default="user")
    name = Column(String(20), unique=True)
    email = Column(String(50), unique=True)
    password = Column(Text)
    posts = relationship("Post", backref="users")
    comments = relationship("Comment", backref="users")


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(ForeignKey("users.id"))
    comments = relationship("Comment", backref="posts")
    title = Column(String(20))
    content = Column(Text)
    # image = Column(BLOB)
    # created_at = Column(TIMESTAMP, nullable=True)
    # modified_at = Column(TIMESTAMP, nullable=True)


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(ForeignKey("posts.id"))
    owner_id = Column(ForeignKey("users.id"))
    text = Column(Text)
    # date = Column(TIMESTAMP)
