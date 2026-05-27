"""Billing Model"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from app.database import Base

class Billing(Base):
    """Billing model"""
    __tablename__ = "billings"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    invoice_number = Column(String(50), unique=True, index=True)
    amount = Column(Float)
    status = Column(String(20), default="pending")
    due_date = Column(DateTime)
    paid_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
