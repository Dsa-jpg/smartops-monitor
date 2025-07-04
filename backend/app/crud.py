from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from app.config import SECRETE_KEY, ALGORTITHM, ACCESS_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

# --- Users ---
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_psw = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_psw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# --- Services ---
def get_service(db: Session, service_id: int):
    return db.query(models.Service).filter(models.Service.id == service_id).first()

def get_services_by_id(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Service)
        .filter(models.Service.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_service(db: Session, service_in: schemas.ServiceCreate, user: models.User) -> models.Service:
    service = models.Service(**service_in.dict(), owner_id=user.id)
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

def update_service_status(db: Session, service_id: int, status_code: int):
    service = get_service(db, service_id)
    if service:
        service.status = status_code
        db.commit()
        db.refresh(service)



def add_service_status_history(db: Session, service_id: int, status_code: int):
    history_entry = models.ServiceStatusHistory(
        service_id=service_id,
        status=status_code,
        timestamp=datetime.utcnow()
    )
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)
    return history_entry

# --- Alerts ---
def get_alert(db: Session, alert_id: int):
    return db.query(models.Alert).filter(models.Alert.id == alert_id).first()

def get_alerts(db: Session, user_id = int):
    return (
        db.query(models.Alert)
        .join(models.Service)
        .filter(models.Service.owner_id == user_id)
        .all()
    )

def create_alert(db: Session, alert_in: schemas.AlertCreated) -> models.Alert:
    alert = models.Alert(**alert_in.dict())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert



# --- Auth/Login ---
def hash_pass(password: str):
    return pwd_context.hash(password)

def verify_pass(plain_pass : str, hashed_password: str):
    return pwd_context.verify(plain_pass, hashed_password)

def create_acc_token(data: dict, exprires_delta: timedelta = None):

    to_encode = data.copy()
    expire = datetime.now() + (exprires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORTITHM)

def auth_user (db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_pass(password,user.hashed_password):
        return False
    return user
