from pydantic import BaseModel
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(Post):
    pass

class PostResponse(Post):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class User(BaseModel):
    email: str
    password: str

class UserCreate(User):
    pass

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True