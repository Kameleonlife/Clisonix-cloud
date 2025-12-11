#!/usr/bin/env python
"""
Minimal test to isolate the issue
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/test")
def test_endpoint():
    logger.info("Handler called!")
    return {"status": "ok"}

if __name__ == "__main__":
    logger.info("Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=False, access_log=True)
