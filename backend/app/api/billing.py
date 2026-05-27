"""Billing API Routes"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.billing import BillingCreate, BillingResponse
from app.models.billing import Billing

router = APIRouter()

@router.post("/", response_model=BillingResponse)
async def create_billing(billing: BillingCreate, db: Session = Depends(get_db)):
    """Create a new billing record"""
    db_billing = Billing(**billing.dict())
    db.add(db_billing)
    db.commit()
    db.refresh(db_billing)
    return db_billing

@router.get("/{billing_id}", response_model=BillingResponse)
async def get_billing(billing_id: int, db: Session = Depends(get_db)):
    """Get billing by ID"""
    billing = db.query(Billing).filter(Billing.id == billing_id).first()
    return billing

@router.get("/", response_model=list[BillingResponse])
async def list_billings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """List all billing records"""
    billings = db.query(Billing).offset(skip).limit(limit).all()
    return billings
