from jose import jwt
from fastapi import HTTPException, Depends, status
from . import token
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

# here login is the route path
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(data: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token.verify_token(data, credentials_exception)