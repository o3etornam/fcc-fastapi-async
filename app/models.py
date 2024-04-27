from datetime import datetime
from sqlalchemy import Integer, Boolean, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.sql.expression import text

# from .database import Base

class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    published: Mapped[bool] = mapped_column(Boolean,server_default='TRUE', default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    user_id: Mapped[int] = mapped_column(Integer,ForeignKey(column="users.id",ondelete="cascade"),nullable=False,)

    user: Mapped["User"] = relationship('User')
    

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, autoincrement=True)
    email: Mapped[str] = mapped_column(String, nullable=False,unique=True)
    password: Mapped[str] = mapped_column(String, nullable= False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    
class Vote(Base):
    __tablename__ = 'votes'

    user_id: Mapped[int] = mapped_column(Integer,  ForeignKey(column="users.id", ondelete="cascade"), primary_key=True,nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey(column="posts.id", ondelete="cascade"), primary_key=True, nullable=False)





