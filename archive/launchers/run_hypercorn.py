#!/usr/bin/env python
"""
Direct FastAPI startup - bypasses uvicorn reload issues
"""
import asyncio
from apps.api.main import app
from hypercorn.asyncio import serve
from hypercorn.config import Config

async def main():
    config = Config()
    config.bind = ["127.0.0.1:8000"]
    await serve(app, config)

if __name__ == "__main__":
    asyncio.run(main())
