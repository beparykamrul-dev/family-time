"""Employee API Routes"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_employees():
    """List all employees"""
    return {"employees": []}

@router.get("/{employee_id}")
async def get_employee(employee_id: int):
    """Get employee by ID"""
    return {"id": employee_id, "name": "Employee"}
