from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud
from app.db import get_db
from app.security import get_current_user


router = APIRouter(prefix="/users",tags=["users"])

@router.post("/",response_model=schemas.UserRead,status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db,email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registred")
    return crud.create_user(db, user_in)
    
@router.get("/user-info", response_model=schemas.UserRead)
def read_user(user: schemas.UserRead = Depends(get_current_user), db: Session = Depends(get_db)):
    return user

@router.get("/",response_model=List[schemas.UserRead])
def read_users(skip: int, limit: int, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users