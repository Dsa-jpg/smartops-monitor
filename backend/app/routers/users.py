from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud
from app.db import get_db


router = APIRouter(prefix="/users",tags=["users"])

@router.post("/",response_model=schemas.UserRead,status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db,email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registred")
    return crud.create_user(db, user_in)
    
@router.get("/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/",response_model=List[schemas.UserRead])
def read_users(skip: int, limit: int, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users