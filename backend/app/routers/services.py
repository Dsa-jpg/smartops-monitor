from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud, models
from app.db import get_db
from app.security import get_current_user


router = APIRouter(prefix="/services",tags=["services"])

@router.post("/", response_model=schemas.ServiceRead, status_code=status.HTTP_201_CREATED)
def create_service(
    service_in: schemas.ServiceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_service(db, service_in, current_user)
    

@router.get("/",response_model=List[schemas.ServiceRead])
def read_services(skip: int, limit: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_services_by_id(db=db, user_id=current_user.id, skip=skip, limit=limit)