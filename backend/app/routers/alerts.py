from fastapi import APIRouter, Depends, HTTPException, Response, status
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

@router.delete("/{alert_id}", response_model=schemas.AlertRead)
def delete_alert(alert_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    alert = (
        db.query(models.Alert)
        .join(models.Alert.service)
        .filter(
            models.Alert.id == alert_id,
            models.Service.owner_id == current_user.id
        )
        .first()
    )
    
    if alert is None:
        raise HTTPException(status_code=404, detail="Alert not found or not authorized")
    
    db.delete(alert)
    db.commit()
    
    return Response(status_code=204)

@router.patch("/{alert_id}", response_model=schemas.AlertRead)
def update_alert(alert_id: int, alert_in : schemas.AlertUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    alert = db.query(models.Alert).filter_by(id=alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    service = db.query(models.Service).filter_by(id=alert.service_id, owner_id=current_user.id).first()
    if service is None:
        raise HTTPException(status_code=403, detail="Not authorized to delete this alert.")
    for key, value in alert_in.model_dump(exclude_unset=True).items():
        setattr(alert, key, value)

    db.commit()
    db.refresh(alert)
    return alert