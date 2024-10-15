from fastapi import status, Response, APIRouter, Depends
from .. import schemas, database, oAuth2
from typing import List
from ..controllers import blog

router = APIRouter(
    tags=['Blogs'],
    prefix='/blog'
    )

# create a blog
@router.post("/", status_code=status.HTTP_201_CREATED)
def createBlog(request: schemas.Blog, db: database.db_dependency, current_user: schemas.User = Depends(oAuth2.get_current_user)):
    return blog.create(request, db)

# get all blogs 
# we are getting a list of blogs where each blog is of ShowBLog type response body
@router.get("/", response_model=List[schemas.ShowBlog])
def getBlogs(db: database.db_dependency, current_user: schemas.User = Depends(oAuth2.get_current_user)):
    return blog.getAll(db)

# get blog by id
# FastAPI sees Depends(oAuth2.get_current_user) and knows it needs to call get_current_user before it executes the below function.
# get_current_user is executed every time a request is made to this endpoint.
@router.get("/{blog_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def getBlogById(blog_id:int, response: Response, db:database.db_dependency, current_user: schemas.User = Depends(oAuth2.get_current_user)):
    return blog.show(blog_id, response, db)
    
# delete a blog by id
@router.delete("/{blog_id}", status_code=status.HTTP_200_OK)
def deleteBlogById(blog_id:int, response: Response, db:database.db_dependency, current_user: schemas.User = Depends(oAuth2.get_current_user)):
    return blog.destroy(blog_id, response, db)

# update a blog by id
@router.put("/{blog_id}", status_code=status.HTTP_200_OK)
def updateBlog(blog_id:int, request: schemas.Blog, response:Response, db:database.db_dependency, current_user: schemas.User = Depends(oAuth2.get_current_user)):
    return blog.update(blog_id, request, response, db)