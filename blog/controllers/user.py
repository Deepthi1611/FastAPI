from .. import schemas, models
from sqlalchemy.orm import Session
from ..hashing import Hash
from fastapi import HTTPException

def create(request: schemas.User, db: Session):
    new_user = models.User( name=request.name,
    email=request.email,
    password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'detail': 'User created successfully', 'user': new_user}

def show(user_id:int, db: Session):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found with given id')
    return user