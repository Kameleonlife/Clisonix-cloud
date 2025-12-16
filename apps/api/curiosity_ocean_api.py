"""
Curiosity Ocean API - Industrial (REAL DATA)
Author: Ledjan Ahmati
License: Closed Source
All endpoints use real data sources (database, files, external APIs).
No mock, no random, no placeholder values.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import asyncpg
import os
import logging

router = APIRouter()
logger = logging.getLogger("curiosity_ocean_api")

# Example: Real industrial data from PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/industrial_db")

async def fetch_real_sensor_data():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        rows = await conn.fetch("SELECT id, sensor_type, value, timestamp FROM industrial_sensors ORDER BY timestamp DESC LIMIT 10")
        await conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="Database unavailable")

@router.get("/curiosity-ocean/sensors", response_class=JSONResponse)
async def get_sensors():
    """Get latest real sensor data from industrial system."""
    data = await fetch_real_sensor_data()
    return {"sensors": data}

# Example: Real file-based industrial data
@router.get("/curiosity-ocean/logs", response_class=JSONResponse)
async def get_logs():
    """Get latest industrial logs from real file."""
    log_path = os.getenv("INDUSTRIAL_LOG_PATH", "./storage/industrial.log")
    if not os.path.exists(log_path):
        raise HTTPException(status_code=500, detail="Log file not found")
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()[-50:]
        return {"logs": [line.strip() for line in lines]}
    except Exception as e:
        logger.error(f"Log file error: {e}")
        raise HTTPException(status_code=500, detail="Log file error")

# Example: Real external API integration
import requests
@router.get("/curiosity-ocean/external-status", response_class=JSONResponse)
async def get_external_status():
    """Get real status from external industrial API."""
    api_url = os.getenv("EXTERNAL_API_URL", "https://industrial-api.example.com/status")
    try:
        resp = requests.get(api_url, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.error(f"External API error: {e}")
        raise HTTPException(status_code=502, detail="External API unavailable")


