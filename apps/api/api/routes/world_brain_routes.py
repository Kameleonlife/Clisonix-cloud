"""
World Brain Routes - Industrial API
Author: Ledjan Ahmati
License: Closed Source
"""

from fastapi import APIRouter, HTTPException
import time
import psutil

router = APIRouter()

@router.get("/world-brain/status", tags=["World Brain"])
def get_world_brain_status():
    """Kthen statusin real të World Brain industrial."""
    return {
        "status": "active",
        "timestamp": time.time(),
        "cpu_percent": psutil.cpu_percent(),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage("/")._asdict(),
        "hostname": psutil.users()[0].name if psutil.users() else "unknown"
    }

@router.get("/world-brain/metrics", tags=["World Brain"])
def get_world_brain_metrics():
    """Kthen metrika reale të World Brain industrial."""
    return {
        "uptime": time.time() - psutil.boot_time(),
        "process_count": len(psutil.pids()),
        "load_avg": psutil.getloadavg() if hasattr(psutil, "getloadavg") else None,
        "timestamp": time.time()
    }


