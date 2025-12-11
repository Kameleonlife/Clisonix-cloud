"""
Clisonix Cloud - Minimal FastAPI Backend
Reduced resource usage for Docker deployment
"""

import os
import logging
from fastapi import Depends
from fastapi import Request
from usage_tracker import increment_usage, get_usage
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Clisonix Cloud - Minimal",
    description="Lightweight API for reduced PC load",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check(request: Request):
    """Health check endpoint"""
    api_key = request.headers.get("x-api-key")
    if api_key:
        increment_usage(api_key)
    return {
        "status": "healthy",
        "service": "Clisonix Cloud Minimal",
        "version": "1.0.0",
        "load_type": "minimal"
    }

@app.get("/")
async def root(request: Request):
    """Root endpoint"""
    api_key = request.headers.get("x-api-key")
    if api_key:
        increment_usage(api_key)
    return {
        "message": "Clisonix Cloud - Minimal Load Setup",
        "status": "running",
        "endpoints": ["/health", "/status", "/system", "/usage"]
    }

@app.get("/status")
async def system_status(request: Request):
    """System status with minimal resource usage"""
    try:
        api_key = request.headers.get("x-api-key")
        if api_key:
            increment_usage(api_key)
        return {
            "system": "operational",
            "containers": "minimal_setup",
            "resource_usage": "low",
            "pc_load": "reduced"
        }
    except Exception as e:
        logger.error(f"Status check error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/system")
async def system_info(request: Request):
    """Basic system information"""
    api_key = request.headers.get("x-api-key")
    if api_key:
        increment_usage(api_key)
    return {
        "backend": "FastAPI",
        "deployment": "Docker Minimal",
        "purpose": "PC Load Reduction",
        "memory_target": "< 512MB",
        "cpu_target": "< 1 core"
    }
@app.get("/usage")
async def usage_stats(request: Request):
    """Get API key usage for today"""
    api_key = request.headers.get("x-api-key")
    if not api_key:
        raise HTTPException(status_code=400, detail="Missing x-api-key header")
    usage = get_usage(api_key)
    return {"api_key": api_key, "usage_today": usage}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# Stripe billing endpoints
from stripe_integration import create_customer, create_subscription, get_customer_usage

@app.post("/billing/customer")
async def billing_create_customer(email: str, name: str = None):
    customer = create_customer(email, name)
    return {"customer": customer}

@app.post("/billing/subscription")
async def billing_create_subscription(customer_id: str, price_id: str):
    subscription = create_subscription(customer_id, price_id)
    return {"subscription": subscription}

@app.get("/billing/usage")
async def billing_usage(customer_id: str):
    usage = get_customer_usage(customer_id)
    return usage