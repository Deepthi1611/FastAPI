from fastapi import APIRouter, HTTPException
from .. import schemas, database, models
from ..hashing import Hash

router = APIRouter(
    tags=['Users'],
    prefix='/user'
)

# create a user
@router.post('/')
def createUser(request: schemas.User,  db:database.db_dependency):
    new_user = models.User( name=request.name,
    email=request.email,
    password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'detail': 'User created successfully', 'user': new_user}

# get user by id
@router.get("/{user_id}", response_model=schemas.ShowUser)
def getUser(user_id: int, db:database.db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found with given id')
    return user