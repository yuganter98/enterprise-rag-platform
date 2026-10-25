from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class Role(RoleBase):
    id: int
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True

class UserCreate(UserBase):
    password: str
    role_id: Optional[int] = None  # Defaults to the 'employee' role when omitted

class UserResponse(UserBase):
    id: int
    role: Optional[Role] = None

    class Config:
        from_attributes = True
