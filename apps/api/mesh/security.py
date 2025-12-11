import time
import threading
from fastapi import Request

class DDoSGuardMiddleware:
    """Simple token-bucket per-IP rate limiter used as ASGI middleware."""
    def __init__(self, app, rate=5, per=1.0):
        self.app = app
        self.rate = rate
        self.per = per
        self.tokens = {}
        self.lock = threading.Lock()

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return
        client = scope.get("client")
        ip = client[0] if client else "unknown"
        now = time.time()
        with self.lock:
            tok = self.tokens.get(ip, {"t": now, "c": self.rate})
            elapsed = now - tok["t"]
            tok["t"] = now
            tok["c"] = min(self.rate, tok["c"] + elapsed * (self.rate / self.per))
            if tok["c"] < 1:
                # drop
                from starlette.responses import PlainTextResponse
                resp = PlainTextResponse("Rate limit", status_code=429)
                await resp(scope, receive, send)
                return
            tok["c"] -= 1
            self.tokens[ip] = tok
        await self.app(scope, receive, send)

def verify_request_hmac(request: Request, key: str) -> bool:
    # placeholder: real implementation would verify signature header
    return True
