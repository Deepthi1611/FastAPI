from . import schemas, models
from fastapi import FastAPI
from .routers import blog, user
from .database import engine

app = FastAPI()

# create all models when server is being run
models.Base.metadata.create_all(engine)

app.include_router(blog.router)
app.include_router(user.router)
