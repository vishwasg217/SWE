from .database import engine, get_db
from . import models
from .utils import hash
from .schemas import PostCreate, PostResponse, UserCreate, UserResponse
from .routers import post, user

from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session


# creates new tables in the database if they don't exist
models.Base.metadata.create_all(bind=engine)




app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
