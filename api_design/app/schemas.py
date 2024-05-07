from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    

class UserCreate(User):
    pass

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(Post):
    pass

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    author_id: int
    author: UserResponse

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None