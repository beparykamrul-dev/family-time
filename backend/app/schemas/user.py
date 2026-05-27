"""User Schemas"""

from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    """User creation schema"""
    username: str
    email: EmailStr
    full_name: str
    password: str

class UserResponse(BaseModel):
    """User response schema"""
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
