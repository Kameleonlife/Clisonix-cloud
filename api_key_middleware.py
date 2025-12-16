from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import os, json

API_KEYS_FILE = "config/api_keys.json"

def load_api_keys():
    try:
        with open(API_KEYS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/auth") or request.url.path.startswith("/docs"):
            return await call_next(request)
        api_key = request.headers.get("x-api-key")
        if not api_key:
            raise HTTPException(status_code=401, detail="Missing x-api-key header")
        valid_keys = load_api_keys()
        if api_key not in valid_keys.values():
            raise HTTPException(status_code=403, detail="Invalid API key")
        response = await call_next(request)
        return response

