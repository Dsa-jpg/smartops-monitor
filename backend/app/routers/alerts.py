from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud, models
from app.db import get_db
from app.security import get_current_user


router = APIRouter(prefix="/alerts",tags=["alerts"])

@router.post("/", response_model=schemas.AlertRead, status_code=status.HTTP_201_CREATED)
def create_alert(
    alert_in: schemas.AlertCreated,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    
    service = db.query(models.Service).filter_by(id=alert_in.service_id, owner_id=current_user.id).first()
    if service is None:
        raise HTTPException(status_code=403, detail="Service does not belong to the current user.")
    
    return crud.create_alert(db, alert_in)


@router.get("/",response_model=List[schemas.AlertRead])
def read_alerts_by_user(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.get_alerts(db=db, user_id=current_user.id)