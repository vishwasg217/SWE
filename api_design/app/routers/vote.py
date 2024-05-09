from ..database import get_db
from .. import models
from ..schemas import Vote
from ..oauth2 import get_current_user

from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Vote"]
)

@router.post("/vote", status_code=status.HTTP_201_CREATED)
def vote_post(vote: Vote, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    user_id = current_user.user_id

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first() 

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {vote.post_id} not found."
        )
    
    vote_query = db.query(models.Vote).filter(models.Vote.user_id == user_id, models.Vote.post_id == vote.post_id)
    existing_vote = vote_query.first()

    if vote.vote_dir == True:
        if existing_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User has already upvoted this post."
            )

        new_vote = models.Vote(user_id=current_user.user_id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()    

        return {"message": "Upvoted successfully."}
    else:
        if existing_vote:
            db.delete(existing_vote)
            db.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User has not upvoted this post."
            )
        
        return {"message": "Deleted vote successfully."}
    
        

