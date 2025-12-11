"""
╔════════════════════════════════════════════════════════════════════╗
║     CLISONIX CLOUD - SAAS SERVICES ORCHESTRATOR                    ║
║     Ports: 5555-7777 (Dynamic Service Discovery & Mesh)            ║
║     All components active and interconnected                        ║
╚════════════════════════════════════════════════════════════════════╝

This orchestrator manages:
- ALBA Collector (5555) - Network telemetry
- ALBI Processor (6666) - Neural analytics
- JONA Coordinator (7777) - Data synthesis
- Mesh HQ (Fallback on 7778) - Node management
- Service registry & health checks
- Inter-service communication
"""

import asyncio
import json
import time
import uuid
import logging
import socket
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from pathlib import Path
import os

from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn
import aiohttp

# OpenTelemetry imports
from tracing import setup_tracing, instrument_fastapi_app, instrument_http_clients

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SaasOrchestrator")

# Initialize tracing
tracer = setup_tracing("orchestrator")

SERVICE_PORTS = {
    "alba": 5555,      # Network telemetry collector
    "albi": 6666,      # Neural analytics processor
    "jona": 7777,      # Data synthesis coordinator
    "mesh": 7778,      # Mesh network orchestrator
}

# Support both localhost (dev) and container hostnames (Docker)
_alba_host = os.getenv("SERVICE_ALBA_HOST", "localhost")
_albi_host = os.getenv("SERVICE_ALBI_HOST", "localhost")
_jona_host = os.getenv("SERVICE_JONA_HOST", "localhost")
_mesh_host = os.getenv("SERVICE_MESH_HOST", "localhost")

SERVICE_URLS = {
    "alba": f"http://{_alba_host}:{SERVICE_PORTS['alba']}",
    "albi": f"http://{_albi_host}:{SERVICE_PORTS['albi']}",
    "jona": f"http://{_jona_host}:{SERVICE_PORTS['jona']}",
    "mesh": f"http://{_mesh_host}:{SERVICE_PORTS['mesh']}",
}

INSTANCE_ID = uuid.uuid4().hex[:8]
START_TIME = time.time()

# ═══════════════════════════════════════════════════════════════════
# SCHEMAS
# ═══════════════════════════════════════════════════════════════════

class ServiceInfo(BaseModel):
    name: str
    port: int
    status: str = "unknown"
    health: float = 0.0
    uptime_seconds: float = 0.0
    endpoint: str = ""
    last_check: str = ""

class ServiceRegistryData(BaseModel):
    """Data model for service registry response"""
    timestamp: str
    instance_id: str
    services: Dict[str, ServiceInfo]
    total_services: int
    healthy_count: int

class DataPacket(BaseModel):
    """Inter-service communication packet"""
    source: str
    destination: str
    packet_type: str  # "telemetry", "analytics", "synthesis", "heartbeat"
    payload: Dict[str, Any]
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    correlation_id: str = Field(default_factory=uuid.uuid4().hex)

class ServiceRequest(BaseModel):
    service: str
    action: str
    parameters: Dict[str, Any] = {}

class HealthStatus(BaseModel):
    service: str
    status: str
    health_score: float
    message: str
    timestamp: str

# ═══════════════════════════════════════════════════════════════════
# SERVICE REGISTRY & DISCOVERY
# ═══════════════════════════════════════════════════════════════════

class ServiceRegistry:
    """Manages service discovery and health checks"""
    
    def __init__(self):
        self.services: Dict[str, ServiceInfo] = {
            name: ServiceInfo(
                name=name,
                port=port,
                endpoint=SERVICE_URLS.get(name, f"http://localhost:{port}")
            )
            for name, port in SERVICE_PORTS.items()
        }
        self.health_checks: Dict[str, float] = {}
        self.communication_log: List[DataPacket] = []
    
    async def check_service_health(self, name: str, url: str) -> Dict[str, Any]:
        """Check if service is responding"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}/health", timeout=aiohttp.ClientTimeout(total=2)) as resp:
                    if resp.status == 200:
                        return {
                            "status": "online",
                            "health": 1.0,
                            "response_code": resp.status
                        }
                    else:
                        return {
                            "status": "degraded",
                            "health": 0.5,
                            "response_code": resp.status
                        }
        except asyncio.TimeoutError:
            return {"status": "timeout", "health": 0.2}
        except Exception as e:
            logger.warning(f"Health check failed for {name}: {e}")
            return {"status": "offline", "health": 0.0, "error": str(e)}
    
    async def refresh_all(self):
        """Refresh health status for all services"""
        tasks = [
            self.check_service_health(name, url)
            for name, url in SERVICE_URLS.items()
        ]
        results = await asyncio.gather(*tasks)
        
        for (name, url), result in zip(SERVICE_URLS.items(), results):
            self.services[name].status = result["status"]
            self.services[name].health = result.get("health", 0.0)
            self.services[name].last_check = datetime.now(timezone.utc).isoformat()
    
    def get_registry(self) -> ServiceRegistryData:
        """Get current registry state"""
        healthy = sum(1 for s in self.services.values() if s.status == "online")
        return ServiceRegistryData(
            timestamp=datetime.utcnow().isoformat(),
            instance_id=INSTANCE_ID,
            services=self.services,
            total_services=len(self.services),
            healthy_count=healthy
        )

# ═══════════════════════════════════════════════════════════════════
# FASTAPI APP
# ═══════════════════════════════════════════════════════════════════

app = FastAPI(
    title="Clisonix SaaS Orchestrator",
    version="2.0.0",
    description="Central orchestrator for ALBA, ALBI, JONA, and Mesh services"
)

# Instrument FastAPI app for automatic tracing
instrument_fastapi_app(app, "orchestrator")

# Instrument HTTP clients
instrument_http_clients()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Global registry
registry = ServiceRegistry()

# ═══════════════════════════════════════════════════════════════════
# ENDPOINTS - SERVICE DISCOVERY
# ═══════════════════════════════════════════════════════════════════

@app.get("/registry")
async def get_service_registry():
    """Get current service registry with health status"""
    with tracer.start_as_current_span("get_service_registry") as span:
        await registry.refresh_all()
        reg = registry.get_registry()
        span.set_attribute("services_count", len(reg.services))
        return reg.dict(exclude_none=True)

@app.get("/health")
async def orchestrator_health():
    """Health endpoint for orchestrator itself"""
    with tracer.start_as_current_span("orchestrator_health") as span:
        await registry.refresh_all()
        reg = registry.get_registry()
        span.set_attribute("status", "operational")
        span.set_attribute("healthy_services", reg.healthy_count)
        return {
            "service": "saas-orchestrator",
            "status": "operational",
            "instance_id": INSTANCE_ID,
            "uptime_seconds": time.time() - START_TIME,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "services": reg.dict()
        }

@app.get("/services/{service_name}/health")
async def service_health(service_name: str):
    """Get health status of specific service"""
    with tracer.start_as_current_span("service_health") as span:
        span.set_attribute("service_name", service_name)
        if service_name not in SERVICE_URLS:
            raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
        
        url = SERVICE_URLS[service_name]
        result = await registry.check_service_health(service_name, url)
        
        return HealthStatus(
            service=service_name,
        status=result["status"],
        health_score=result["health"],
        message=result.get("message", ""),
        timestamp=datetime.now(timezone.utc).isoformat()
    ).dict(exclude_none=True)

# ═══════════════════════════════════════════════════════════════════
# ENDPOINTS - INTER-SERVICE COMMUNICATION
# ═══════════════════════════════════════════════════════════════════

@app.post("/communicate")
async def inter_service_communicate(packet: DataPacket):
    """Route communication between services"""
    registry.communication_log.append(packet)
    
    # Keep log size bounded
    if len(registry.communication_log) > 1000:
        registry.communication_log = registry.communication_log[-500:]
    
    dest_url = SERVICE_URLS.get(packet.destination)
    if not dest_url:
        raise HTTPException(
            status_code=404,
            detail=f"Destination service '{packet.destination}' not found"
        )
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{dest_url}/receive",
                json=packet.dict(),
                timeout=aiohttp.ClientTimeout(total=5)
            ) as resp:
                response_data = await resp.json()
                return {
                    "status": "delivered",
                    "correlation_id": packet.correlation_id,
                    "response": response_data
                }
    except Exception as e:
        logger.error(f"Communication error: {e}")
        raise HTTPException(status_code=502, detail=f"Failed to reach destination: {str(e)}")

@app.get("/communication/log")
async def get_communication_log(limit: int = 50):
    """Get recent inter-service communication log"""
    recent = registry.communication_log[-limit:]
    return {
        "total_logged": len(registry.communication_log),
        "recent": [p.dict() for p in recent]
    }

# ═══════════════════════════════════════════════════════════════════
# ENDPOINTS - SERVICE CONTROL
# ═══════════════════════════════════════════════════════════════════

@app.post("/services/{service_name}/execute")
async def execute_service_action(service_name: str, request: ServiceRequest):
    """Execute action on a specific service"""
    if service_name not in SERVICE_URLS:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    
    url = SERVICE_URLS[service_name]
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{url}/execute",
                json=request.dict(),
                timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                result = await resp.json()
                return {
                    "service": service_name,
                    "action": request.action,
                    "status": "executed",
                    "result": result
                }
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Service error: {str(e)}")

# ═══════════════════════════════════════════════════════════════════
# ENDPOINTS - AGGREGATED METRICS
# ═══════════════════════════════════════════════════════════════════

@app.get("/metrics/aggregated")
async def aggregated_metrics():
    """Get aggregated metrics from all services"""
    await registry.refresh_all()
    
    metrics = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "orchestrator_uptime": time.time() - START_TIME,
        "services": {}
    }
    
    for name, url in SERVICE_URLS.items():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{url}/metrics", timeout=aiohttp.ClientTimeout(total=2)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        metrics["services"][name] = data
        except Exception:
            metrics["services"][name] = {"status": "unavailable"}
    
    return metrics

@app.get("/status/dashboard")
async def status_dashboard():
    """Get dashboard-friendly status snapshot"""
    await registry.refresh_all()
    reg = registry.get_registry()
    
    service_status = {}
    for name, info in reg.services.items():
        service_status[name] = {
            "port": info.port,
            "status": info.status,
            "health": f"{info.health * 100:.1f}%",
            "url": info.endpoint
        }
    
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "instance_id": INSTANCE_ID,
        "orchestrator_uptime_seconds": time.time() - START_TIME,
        "total_services": reg.total_services,
        "healthy_services": reg.healthy_count,
        "services": service_status,
        "communication_log_size": len(registry.communication_log),
        "system_status": "operational" if reg.healthy_count >= reg.total_services - 1 else "degraded"
    }

# ═══════════════════════════════════════════════════════════════════
# BACKGROUND TASKS
# ═══════════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_background_tasks():
    """Start background health check loop"""
    asyncio.create_task(health_check_loop())

async def health_check_loop():
    """Continuously check health of all services"""
    while True:
        try:
            await registry.refresh_all()
            logger.info(f"Health check: {registry.get_registry().healthy_count}/{len(SERVICE_PORTS)} services healthy")
            await asyncio.sleep(10)  # Check every 10 seconds
        except Exception as e:
            logger.error(f"Health check error: {e}")
            await asyncio.sleep(10)

# ═══════════════════════════════════════════════════════════════════
# STARTUP
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    port = int(os.getenv("ORCHESTRATOR_PORT", "9999"))
    print(f"\n╔═══════════════════════════════════════════╗")
    print(f"║  CLISONIX SAAS ORCHESTRATOR              ║")
    print(f"║  Starting on port {port}                     ║")
    print(f"║  Service Registry: http://localhost:{port}/registry")
    print(f"║  Dashboard: http://localhost:{port}/status/dashboard")
    print(f"╚═══════════════════════════════════════════╝\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
