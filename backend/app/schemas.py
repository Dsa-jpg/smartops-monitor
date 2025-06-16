from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime



# --- Alert ---
class AlertBase(BaseModel):
    level: str
    message: str

class AlertCreated(AlertBase):
    service_id: int

class AlertRead(AlertBase):
    id: int
    timestamp: datetime

    class Config:
        from_atrributes = True

# --- Service ---

class ServiceBase(BaseModel):
    name: str
    url: str

class ServiceCreate(ServiceBase):
    pass

class ServiceRead(ServiceBase):
    id: int
    status: Optional[str]
    alerts: List[AlertRead] = []

    class Config:
        from_atrributes = True

# --- User ---
class UserBase(BaseModel):
    """
    Defines base model options of user in default
    
    """
    email: EmailStr
    
class UserCreate(UserBase):

    password: str

class UserLogin(UserBase):

    password: str

class UserRead(UserBase):

    id: int
    is_active: bool
    services: List[ServiceRead] = []

    class Config:
        from_attributes = True

# --- BearerToken ---
class Token(BaseModel):

    access_token: str
    token_type: str