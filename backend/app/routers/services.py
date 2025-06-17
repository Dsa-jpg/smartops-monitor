from fastapi import APIRouter, Depends, HTTPException, Response, status, Body
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


@router.delete("/{service_id}", response_model=schemas.ServiceRead)
def delete_service(service_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    service = db.query(models.Service).filter_by(id=service_id, owner_id=current_user.id).first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found or not owned by current user")
    db.delete(service)
    db.commit()
    return Response(status_code=204)

@router.patch("/{service_id}", response_model=schemas.ServiceRead)
def update_service(service_id: int,service_in: schemas.ServiceUpdate , db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    service = db.query(models.Service).filter_by(id=service_id, owner_id=current_user.id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found or not owned by current user")
    for key, value in service_in.model_dump(exclude_unset=True).items():
        setattr(service, key, value)
    db.commit()
    db.refresh(service)
    return service
   