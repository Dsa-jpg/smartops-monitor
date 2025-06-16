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
