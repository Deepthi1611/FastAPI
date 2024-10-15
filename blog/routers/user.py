from fastapi import APIRouter
from .. import schemas, database, models
from ..hashing import Hash
from ..controllers import user

router = APIRouter(
    tags=['Users'],
    prefix='/user'
)

# create a user
@router.post('/')
def createUser(request: schemas.User,  db:database.db_dependency):
    return user.create(request, db)

# get user by id
@router.get("/{user_id}", response_model=schemas.ShowUser)
def getUser(user_id: int, db:database.db_dependency):
    return user.show(user_id, db)