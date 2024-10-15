from fastapi import status, Response, APIRouter
from .. import schemas, database, models
from typing import List

router = APIRouter(
    tags=['Blogs'],
    prefix='/blog'
    )

# create a blog
@router.post("/", status_code=status.HTTP_201_CREATED)
def createBlog(blog: schemas.Blog, db: database.db_dependency):
    new_blog = models.Blog(title = blog.title, body = blog.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {'message': 'Blog created successfully'}

# get all blogs 
# we are getting a list of blogs where each blog is of ShowBLog type response body
@router.get("/", response_model=List[schemas.ShowBlog])
def getBlogs(db: database.db_dependency):
    blogs = db.query(models.Blog).all()
    return blogs

# get blog by id
@router.get("/{blog_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog)
def getBlogById(blog_id:int, response: Response, db:database.db_dependency):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'detail': f'blog with id: {blog_id} is not found'}
    else:
        return blog
    
# delete a blog by id
@router.delete("/{blog_id}", status_code=status.HTTP_200_OK)
def deleteBlogById(blog_id:int, response: Response, db:database.db_dependency):
    # blog = db.query(models.Blog).filter(models.Blog.id == blog_id).delete(synchronize_session=False)
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog is None:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'detail': 'blog with given id is not found'}
    db.delete(blog)
    db.commit()
    return {'detail': 'blog deleted successfully'}

# update a blog by id
@router.put("/{blog_id}", status_code=status.HTTP_200_OK)
def updateBlog(blog_id:int, request: schemas.Blog, response:Response, db:database.db_dependency):
    # db.query(models.Blog).filter(models.Blog.id == blog_id).update(request)
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