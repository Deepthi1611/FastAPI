from fastapi import FastAPI, Depends, HTTPException, status, Response
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
@app.post("/blog", status_code=status.HTTP_201_CREATED)
def createBlog(blog: schemas.Blog, db: db_dependency):
    new_blog = models.Blog(title = blog.title, body = blog.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {'message': 'Blog created successfully'}

# get all blogs 
@app.get("/blogs")
def getBlogs(db: db_dependency):
    blogs = db.query(models.Blog).all()
    return {"blogs": blogs}

# get blog by id
@app.get("/blog/{blog_id}", status_code=status.HTTP_200_OK)
def getBlogById(blog_id:int, response: Response, db:db_dependency):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'detail': f'blog with id: {blog_id} is not found'}
    else:
        return {"blog": blog}
    
# delete a blog by id
@app.delete("/blog/{blog_id}", status_code=status.HTTP_200_OK)
def deleteBlogById(blog_id:int, response: Response, db:db_dependency):
    # blog = db.query(models.Blog).filter(models.Blog.id == blog_id).delete(synchronize_session=False)
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog is None:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'detail': 'blog with given id is not found'}
    db.delete(blog)
    db.commit()
    return {'detail': 'blog deleted successfully'}

# update a blog by id
@app.put("/blog/{blog_id}", status_code=status.HTTP_200_OK)
def updateBlog(blog_id:int, request: schemas.Blog, response:Response, db:db_dependency):
    # Update the blog entry
    update_query = db.query(models.Blog).filter(models.Blog.id == blog_id)
    
    # Check if the blog exists
    if not update_query.first(): 
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': 'Blog not found with the given ID'}
    
    # Apply the update
    blog_data = request.dict(exclude_unset=True)
    update_query.update(blog_data)
    
    # Commit the changes to the database
    db.commit()
    
    return {'detail': 'Blog updated successfully'}