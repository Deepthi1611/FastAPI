from .. import models, schemas
from sqlalchemy.orm import Session
from fastapi import status, Response

def getAll(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def create(request: schemas.Blog, db:Session):
    new_blog = models.Blog(title = request.title, body = request.body, user_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {'message': 'Blog created successfully'}

def destroy(blog_id: int, response: Response, db: Session):
    # blog = db.query(models.Blog).filter(models.Blog.id == blog_id).delete(synchronize_session=False)
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog is None:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'detail': 'blog with given id is not found'}
    db.delete(blog)
    db.commit()
    return {'detail': 'blog deleted successfully'}

def update(blog_id: int, request: schemas.Blog, response: Response, db: Session):
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

def show(blog_id: int, response: Response, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        response.status_code=status.HTTP_404_NOT_FOUND
        return {'detail': f'blog with id: {blog_id} is not found'}
    else:
        return blog