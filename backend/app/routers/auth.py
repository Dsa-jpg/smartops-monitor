from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, crud
from app.db import get_db

router = APIRouter(tags=["auth"])

@router.post("/register",response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db,user_in.email):
        raise HTTPException(status_code=400, detail="Email already registred.")
    return crud.create_user(db, user_in)

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.auth_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = crud.create_acc_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

    