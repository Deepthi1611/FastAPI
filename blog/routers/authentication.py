from fastapi import APIRouter, Depends
from .. import schemas, database
from ..controllers import authentication
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session 

router = APIRouter(
    tags=['Login'],
    prefix='/login'
)

@router.post("/")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session =  Depends(database.get_db)):
     return authentication.userLogin(request, db)