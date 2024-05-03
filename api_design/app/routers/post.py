from ..database import engine, get_db
from .. import models
from ..utils import hash
from ..schemas import PostCreate, PostResponse

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "success"}

@router.get("/posts", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=404, 
            detail=f"Post with ID {post_id} not found."
        )
    return post

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(payload: PostCreate, db: Session = Depends(get_db)):
    
    new_post = models.Post(**payload.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
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
    
@router.put("/posts/{post_id}", response_model=PostResponse)
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