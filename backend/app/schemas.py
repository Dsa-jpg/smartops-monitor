from pydantic import BaseModel, EmailStr




class UserBase(BaseModel):
    """
    Defines base model options of user in default
    
    """
    email: EmailStr
    
class UserCreate(UserBase):

    password: str


class UserRead(UserBase):

    id: int
    is_active: bool
    # services

    class Config:
        from_attributes = True