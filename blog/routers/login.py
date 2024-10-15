from fastapi import APIRouter
from .. import schemas, database
from ..controllers import authentication

router = APIRouter(
    tags=['Login'],
    prefix='/login'
)

@router.post("/")
def authentication(request: schemas.Login, db: database.db_dependency):
     return authentication.userLogin(request, db)