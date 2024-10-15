from fastapi import status, Response, APIRouter
from .. import schemas, database, models
from typing import List
from ..controllers import blog

router = APIRouter(
    tags=['Blogs'],
    prefix='/blog'
    )

# create a blog
@router.post("/", status_code=status.HTTP_201_CREATED)
def createBlog(request: schemas.Blog, db: database.db_dependency):
    return blog.create(request, db)

# get all blogs 
# we are getting a list of blogs where each blog is of ShowBLog type response body
@router.get("/", response_model=List[schemas.ShowBlog])
def getBlogs(db: database.db_dependency):
    return blog.getAll(db)

# get blog by id
@router.get("/{blog_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def getBlogById(blog_id:int, response: Response, db:database.db_dependency):
    return blog.show(blog_id, response, db)
    
# delete a blog by id
@router.delete("/{blog_id}", status_code=status.HTTP_200_OK)
def deleteBlogById(blog_id:int, response: Response, db:database.db_dependency):
    return blog.destroy(blog_id, response, db)

# update a blog by id
@router.put("/{blog_id}", status_code=status.HTTP_200_OK)
def updateBlog(blog_id:int, request: schemas.Blog, response:Response, db:database.db_dependency):
    return blog.update(blog_id, request, response, db)