from . import schemas, models
from fastapi import FastAPI
from .routers import authentication, blog, user
from .database import engine

app = FastAPI()

# create all models when server is being run
models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)