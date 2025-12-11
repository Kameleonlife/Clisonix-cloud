# -*- coding: utf-8 -*-
"""
Middleware pÃ«r logim me ngjyra nÃ« Ã§do kÃ«rkesÃ« FastAPI
Business: Ledjan Ahmati - WEB8euroweb GmbH
"""

import time
from typing import Callable, Awaitable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from Clisonix.colored_logger import setup_logger

logger = setup_logger("ClisonixBackend")


class ColoredLoggingMiddleware(BaseHTTPMiddleware):
    """Shfaq kÃ«rkesat dhe pÃ«rgjigjet me ngjyra sipas statusit."""

    def __init__(self, app: ASGIApp, get_response: Callable | None = None) -> None:
        super().__init__(app, dispatch=get_response)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable]):
        start = time.time()
        method = request.method
        path = request.url.path
        client = request.client.host if request.client else "unknown"

        logger.info("âž¡ï¸  %s %s (from %s)", method, path, client)
        try:
            response = await call_next(request)
        except Exception as exc:  # pragma: no cover - runtime safety
            logger.error("ðŸ’¥ Exception in %s %s: %s", method, path, exc)
            raise

        duration_ms = (time.time() - start) * 1000
        status = response.status_code

        if 200 <= status < 300:
            logger.info("âœ… %s %s %s | %.1fms", status, method, path, duration_ms)
        elif 400 <= status < 500:
            logger.warning("âš ï¸ %s %s %s | %.1fms", status, method, path, duration_ms)
        else:
            logger.error("âŒ %s %s %s | %.1fms", status, method, path, duration_ms)

        return response


__all__ = ["ColoredLoggingMiddleware"]
