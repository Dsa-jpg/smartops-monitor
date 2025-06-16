from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jose import JWTError
from app import schemas, crud
from app.db import get_db
from app.config import SECRETE_KEY, ALGORTITHM, ACCESS_TOKEN_EXPIRE_MINUTES



oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login") # needs to be same as the login endpoint 

def get_current_user(token: str = Depends(oauth_scheme), db : Session = Depends(get_db)) -> schemas.UserRead:
    credetials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORTITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credetials_exception
    except JWTError:
        raise credetials_exception
    
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credetials_exception
    return user

