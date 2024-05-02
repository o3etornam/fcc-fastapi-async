from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, conint
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    published: bool
    created_at: datetime = Field(default_factory=datetime.now)
    user: User

    class Config:
        from_attributes = True

class PostPublic(BaseModel):
    Post: Post
    votes: int

    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

    class Config:
        from_attributes = True

class Vote(BaseModel):
    post_id: int
    dir:int =  Field(ge=0, le= 1)