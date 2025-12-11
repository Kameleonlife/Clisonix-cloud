"""
Clisonix Cloud Server
Industrial-Grade Real-Time Middleware System
Business: Ledjan Ahmati - WEB8euroweb GmbH
REAL DATA ONLY â€¢ NO MOCK â€¢ NO RANDOM â€¢ NO FAKE API
"""

from datetime import datetime
import json
import os
import time

import psutil
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.gzip import GZipMiddleware

from Clisonix.middleware import (
    MonitoringMiddleware,
    QuotaGateMiddleware,
    SecurityMiddleware,
)

app = FastAPI(
    title="Clisonix Cloud API",
    description="Real-time AI & Sensor Middleware System",
    version="3.0.0-industrial",
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(QuotaGateMiddleware)
app.add_middleware(SecurityMiddleware)
app.add_middleware(MonitoringMiddleware)


@app.get("/status")
async def system_status():
    """Return real-time host metrics."""

    net_io = psutil.net_io_counters()
    stats = {
        "timestamp": datetime.utcnow().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=None),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
        "net_io": {
            "sent_MB": round(net_io.bytes_sent / (1024**2), 2),
            "recv_MB": round(net_io.bytes_recv / (1024**2), 2),
        },
        "active_processes": len(psutil.pids()),
        "uptime_sec": round(time.time() - psutil.boot_time()),
    }
    return JSONResponse({"status": "ok", "metrics": stats})


@app.get("/ping")
async def ping():
    return {"message": "Clisonix active", "time": datetime.utcnow().isoformat()}


@app.post("/metrics/upload")
async def upload_metrics(request: Request):
    """Persist incoming metric payloads to disk."""

    data = await request.json()
    target_dir = os.path.join("cloud_data")
    os.makedirs(target_dir, exist_ok=True)
    with open(os.path.join(target_dir, "metrics.jsonl"), "a", encoding="utf-8") as handle:
        handle.write(json.dumps(data) + "\n")
    return JSONResponse({"ok": True, "timestamp": datetime.utcnow().isoformat()})


if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    import uvicorn

    uvicorn.run("Clisonix_server:app", host="0.0.0.0", port=8080, reload=True)
