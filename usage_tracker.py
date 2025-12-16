import os, json, datetime
import redis
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
try:
    redis_client = redis.from_url(REDIS_URL)
    REDIS_AVAILABLE = True
except Exception:
    REDIS_AVAILABLE = False

USAGE_FILE = "config/api_usage.json"

def load_usage():
    if not os.path.exists(USAGE_FILE):
        return {}
    with open(USAGE_FILE, "r") as f:
        return json.load(f)

def save_usage(data):
    os.makedirs("config", exist_ok=True)
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f, indent=2)

def increment_usage(api_key: str) -> int:
    today = datetime.date.today().isoformat()
    key = f"usage:{api_key}:{today}"
    if REDIS_AVAILABLE:
        count = redis_client.incr(key)
        redis_client.expire(key, 86400)
        return int(count)
    else:
        data = load_usage()
        data.setdefault(api_key, {}).setdefault(today, 0)
        data[api_key][today] += 1
        save_usage(data)
        return data[api_key][today]

def get_usage(api_key: str):
    today = datetime.date.today().isoformat()
    if REDIS_AVAILABLE:
        val = redis_client.get(f"usage:{api_key}:{today}")
        return int(val or 0)
    data = load_usage()
    return data.get(api_key, {}).get(today, 0)

