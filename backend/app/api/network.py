"""Network API Routes"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/status")
async def network_status():
    """Get network status"""
    return {"status": "online", "devices": 0}

@router.get("/devices")
async def list_devices():
    """List all network devices"""
    return {"devices": []}
