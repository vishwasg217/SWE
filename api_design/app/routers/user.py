from ..database import engine, get_db
from .. import models
from ..utils import hash
from ..schemas import UserCreate, UserResponse

from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User with ID {user_id} not found."
        )
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(body: UserCreate, db: Session = Depends(get_db)):
    body.password = hash(body.password)

    new_user = models.User(**body.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, body: UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == user_id)
    user = user_query.first()

    if not user:
        raise HTTPException(
            status_code=404, 
            detail=f"User with ID {user_id} not found."
        )    
    
    user_query.update(body.model_dump())
    db.commit()

    return user_query.first()

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
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