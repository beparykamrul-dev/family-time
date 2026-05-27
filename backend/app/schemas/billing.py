"""Billing Schemas"""

from pydantic import BaseModel
from datetime import datetime

class BillingCreate(BaseModel):
    """Billing creation schema"""
    customer_id: int
    invoice_number: str
    amount: float
    due_date: datetime

class BillingResponse(BaseModel):
    """Billing response schema"""
    id: int
    customer_id: int
    invoice_number: str
    amount: float
    status: str
    due_date: datetime
    paid_date: datetime | None
    
    class Config:
        from_attributes = True
