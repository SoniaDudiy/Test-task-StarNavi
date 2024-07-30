import enum
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date, func, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import event

Base = declarative_base()

class Role(enum.Enum):
    admin = "admin"
    moderator = "moderator"
    user = "user"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    avatar = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    roles = Column(Enum(Role), default=Role.moderator)
    confirmed = Column(Boolean, default=False)  # Add this line

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_blocked = Column(Boolean, default=False)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    post = relationship('Post', backref='comments')
    user = relationship('User', backref='comments')

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50), index=True)
    lastname = Column(String(50), index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String(15), unique=True, index=True, nullable=False)
    birthday = Column(Date, default=func.now())
    additional_info = Column(String(150), nullable=True)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), default=1)
    user = relationship('User', backref='contacts', lazy="joined")

@event.listens_for(Contact, 'before_insert')
def updated_favorite(mapper, conn, target):
    if target.firstname.startswith('My'):
        target.is_favorite = True

@event.listens_for(Contact, 'before_update')
def updated_favorite(mapper, conn, target):
    if target.firstname.startswith('My'):
        target.is_favorite = True
