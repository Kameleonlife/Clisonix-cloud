#!/usr/bin/env python3
"""FastAPI service exposing the Earthmind economy metrics layer."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from economy_layer import EconomyLayer

PORT = int(os.getenv("ECONOMY_API_PORT", "9093"))

app = FastAPI(title="Earthmind Economy API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ECONOMY = EconomyLayer(center_name="Zurich-Lab", specialization="neuro-alignment")


class ComputeIn(BaseModel):
    alba_frames: int = 0
    albi_insights: int = 0
    jona_validations: int = 0
    asi_apis: int = 0


@app.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "running", "service": "Economy API", "port": PORT}


@app.get("/")
def root() -> Dict[str, Any]:
    return {
        "status": "running",
        "service": "Economy API",
        "routes": {
            "GET /": "This message",
            "GET /health": "Basic service health",
            "POST /economy/compute": "Compute cycle transaction value",
            "GET /economy/report": "Retrieve latest economy report",
        },
    }


@app.post("/economy/compute")
def compute(payload: ComputeIn) -> Dict[str, Any]:
    tx = ECONOMY.compute_cycle_value(
        alba_frames=payload.alba_frames,
        albi_insights=payload.albi_insights,
        jona_validations=payload.jona_validations,
        asi_apis=payload.asi_apis,
    )
    return {"ok": True, "tx": tx}


@app.get("/economy/report")
def report() -> Dict[str, Any]:
    rep = ECONOMY.generate_report()
    rep["generated_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return rep


if __name__ == "__main__":
    uvicorn.run("economy_api_server:app", host="127.0.0.1", port=PORT, reload=True)

