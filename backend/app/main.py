"""FastAPI Application Entry Point"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import engine, Base
from app.api import customers, billing, network, employees

# Create tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Application starting...")
    yield
    # Shutdown
    print("Application shutting down...")

app = FastAPI(
    title="ISP-OS API",
    description="AI-Assisted ISP Management Platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(customers.router, prefix="/api/customers", tags=["Customers"])
app.include_router(billing.router, prefix="/api/billing", tags=["Billing"])
app.include_router(network.router, prefix="/api/network", tags=["Network"])
app.include_router(employees.router, prefix="/api/employees", tags=["Employees"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ISP-OS API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
