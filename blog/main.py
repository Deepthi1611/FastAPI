from fastapi import FastAPI, Depends
from . import schemas
from . import models
from .database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session

app = FastAPI()

# create all models when server is being run
models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# create a blog
@app.post("/blog")
def createBlog(blog: schemas.Blog, db: db_dependency):
    new_blog = models.Blog(title = blog.title, body = blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {'message': 'Blog created successfully'}