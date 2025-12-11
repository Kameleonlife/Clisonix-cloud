# -*- coding: utf-8 -*-
"""Shembull pÃ«rdorimi pÃ«r ColoredLoggingMiddleware."""

from fastapi import FastAPI

from Clisonix_backend_logging_middleware import ColoredLoggingMiddleware

app = FastAPI(
    title="Clisonix Industrial Backend (REAL)",
    version="1.0.0",
)

app.add_middleware(ColoredLoggingMiddleware)


@app.get("/health")
async def health():
    return {"ok": True}


@app.get("/status")
async def status():
    return {"system": "stable"}
