from fastapi import APIRouter, Header, HTTPException
import time

router = APIRouter()
USAGE_LOG = {}

@router.post("/record")
def record_usage(x_api_key: str = Header(...)):
    if x_api_key not in [v["api_key"] for v in USAGE_LOG.values()]:
        raise HTTPException(status_code=401, detail="Invalid API key")
    timestamp = int(time.time())
    USAGE_LOG[timestamp] = {"key": x_api_key, "timestamp": timestamp}
    return {"status": "recorded", "timestamp": timestamp}

@router.get("/stats")
def usage_stats():
    return {"usage_records": len(USAGE_LOG), "details": USAGE_LOG}

