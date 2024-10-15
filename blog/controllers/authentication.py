from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..hashing import Hash

def userLogin(request: schemas, db: Session):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found with given email')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid password')
    # generate jwt token
    return user
    