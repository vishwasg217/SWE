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

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}

@app.get("/posts", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=404, 
            detail=f"Post with ID {post_id} not found."
        )
    return post

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    
    new_post = models.Post(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == post_id).delete()
    db.commit()
    if deleted_post:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=404, 
            detail=f"Post with ID {post_id} not found."
        )
    
@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, payload: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=404, 
            detail=f"Post with ID {post_id} not found."
        )    
    
    post_query.update(payload.model_dump())
    db.commit()

    return post_query.first()


@app.get("/users", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User with ID {user_id} not found."
        )
    return user

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    payload.password = hash(payload.password)

    new_user = models.User(**payload.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == user_id)
    user = user_query.first()

    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User with ID {user_id} not found."
        )    
    
    user_query.update(payload.model_dump())
    db.commit()

    return user_query.first()

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    if deleted_user:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(
            status_code=404, 
            detail=f"User with ID {user_id} not found."
        )