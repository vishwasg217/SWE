from ..database import engine, get_db
from .. import models
from ..utils import hash
from ..schemas import UserCreate, UserResponse

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/users", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User with ID {user_id} not found."
        )
    return user

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    payload.password = hash(payload.password)

    new_user = models.User(**payload.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.put("/users/{user_id}", response_model=UserResponse)
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

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
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