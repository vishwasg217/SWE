from .database import engine
from . import models
from .routers import post, user, auth

from fastapi import FastAPI


# creates new tables in the database if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
