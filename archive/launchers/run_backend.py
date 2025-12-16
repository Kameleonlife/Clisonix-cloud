#!/usr/bin/env python
"""
Simple FastAPI startup script for Clisonix Backend
"""
import sys
import signal
import uvicorn

# Ignore terminate signals
signal.signal(signal.SIGTERM, signal.SIG_IGN)
signal.signal(signal.SIGINT, signal.SIG_DFL)

if __name__ == "__main__":
    uvicorn.run(
        "apps.api.main:app",
        host="127.0.0.1",
        port=8000,
        log_level="info",
        access_log=True,
        reload=False,
        workers=1
    )

