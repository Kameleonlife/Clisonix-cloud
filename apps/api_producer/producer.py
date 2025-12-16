"""
API Producer starter stub
- Simple FastAPI app that exposes endpoints to register/publish API metadata
- In-memory store (PRODUCER_DB) for demo purposes
- Lightweight contract:
  - POST /register -> register an API (name, owner, version, description, endpoints)
  - POST /publish -> mark an API as published (manager can consume this)
  - GET /apis -> list registered APIs
  - GET /health -> basic health check

This is a minimal, self-contained file intended as a starting point for the API Producer component.
Run: uvicorn producer:app --reload --port 8001
"""
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Dict, Optional, List
import time

app = FastAPI(title="API Producer (stub)")

# In-memory stores (demo only)
PRODUCER_DB: Dict[str, Dict] = {}
AUDIT_LOG: List[Dict] = []

class ApiMetadata(BaseModel):
    id: str
    name: str
    owner: str
    version: str = "1.0"
    description: Optional[str] = None
    endpoints: Optional[List[str]] = []
    public: bool = False


def audit(event: str, payload: Dict):
    record = {"time": time.time(), "event": event, "payload": payload}
    AUDIT_LOG.append(record)


@app.post("/register")
def register_api(meta: ApiMetadata, x_api_key: Optional[str] = Header(None)):
    """Register a new API metadata entry.
    Optionally check x-api-key for authentication (stub).
    """
    if meta.id in PRODUCER_DB:
        raise HTTPException(status_code=400, detail="API id already exists")
    PRODUCER_DB[meta.id] = meta.dict()
    PRODUCER_DB[meta.id]["registered_at"] = time.time()
    audit("register", {"id": meta.id, "owner": meta.owner})
    return {"status": "registered", "id": meta.id}


@app.post("/publish")
def publish_api(api_id: str, x_api_key: Optional[str] = Header(None)):
    """Mark an API as public/published. API Manager can query Producer for published APIs.
    This is a demo toggle.
    """
    if api_id not in PRODUCER_DB:
        raise HTTPException(status_code=404, detail="API not found")
    PRODUCER_DB[api_id]["public"] = True
    PRODUCER_DB[api_id]["published_at"] = time.time()
    audit("publish", {"id": api_id})
    return {"status": "published", "id": api_id}


@app.get("/apis")
def list_apis(public_only: bool = False):
    """List registered APIs. Use public_only to return only published APIs."""
    items = [v for v in PRODUCER_DB.values() if (not public_only) or v.get("public")]
    return {"count": len(items), "items": items}


@app.get("/apis/{api_id}")
def get_api(api_id: str):
    if api_id not in PRODUCER_DB:
        raise HTTPException(status_code=404, detail="API not found")
    return PRODUCER_DB[api_id]


@app.get("/health")
def health():
    return {"status": "ok", "producer_db_size": len(PRODUCER_DB)}


@app.get("/audit")
def get_audit(limit: int = 100):
    return {"count": len(AUDIT_LOG), "tail": AUDIT_LOG[-limit:]}

