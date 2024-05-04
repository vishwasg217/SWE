from ..database import get_db
from .. import models
from ..utils import verify
from ..schemas import UserLogin

from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session


router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    return {"token": "example token"}