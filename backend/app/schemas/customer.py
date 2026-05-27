"""Customer Schemas"""

from pydantic import BaseModel, EmailStr
from datetime import datetime

class CustomerCreate(BaseModel):
    """Customer creation schema"""
    name: str
    email: EmailStr
    phone: str
    address: str
    package_type: str
    monthly_charge: float

class CustomerResponse(BaseModel):
    """Customer response schema"""
    id: int
    name: str
    email: str
    phone: str
    address: str
    package_type: str
    monthly_charge: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
