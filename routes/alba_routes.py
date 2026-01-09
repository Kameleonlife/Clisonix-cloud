from fastapi import (
    APIRouter, Request, HTTPException, WebSocket, WebSocketDisconnect
)
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import cbor2
import asyncio
from datetime import datetime

router = APIRouter(prefix="/api/alba", tags=["ALBA Data Collection"])


class AlbaStatus(BaseModel):
    module: str
    status: str
    streams_count: int
    streams: List[str]
    data_collection: str
    timestamp: str


class StreamStartRequest(BaseModel):
    stream_id: Optional[str] = Field(
        None, description="Custom stream identifier"
    )
    description: Optional[str] = None
    sampling_rate_hz: Optional[int] = Field(256, ge=1)
    channels: Optional[List[str]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "allow"


class StreamStartResponse(BaseModel):
    message: str
    stream_id: str
    status: str


class StreamStopResponse(BaseModel):
    message: str
    stream_id: str
    status: str


class StreamInfo(BaseModel):
    config: Dict[str, Any]
    start_time: str
    data_points: int
    status: str
    end_time: Optional[str] = None


class StreamsOverview(BaseModel):
    active_streams: Dict[str, StreamInfo]
    total_streams: int


class StreamDataPoint(BaseModel):
    timestamp: str
    channel_1: float
    channel_2: float
    channel_3: float
    signal_quality: float


class StreamDataResponse(BaseModel):
    stream_id: str
    data_points: List[StreamDataPoint]
    metadata: Dict[str, Any]


class CollectionConfigUpdate(BaseModel):
    settings: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "allow"


class CollectionConfigResponse(BaseModel):
    message: str
    new_config: Dict[str, Any]


class CollectionMetrics(BaseModel):
    total_data_points: int
    active_streams: int
    total_streams: int
    data_rate_Hz: int
    storage_usage_mb: float
    uptime_hours: int


class AlbaHealth(BaseModel):
    module: str
    status: str
    timestamp: str
    version: str


# Simulated EEG data streams
active_streams: Dict[str, Dict[str, Any]] = {}
stream_configs: Dict[str, Any] = {}


@router.get("/status", response_model=AlbaStatus)
async def alba_status() -> AlbaStatus:
    """Get ALBA module status"""
    return AlbaStatus(
        module="ALBA",
        status="active",
        streams_count=len(active_streams),
        streams=list(active_streams.keys()),
        data_collection="running",
        timestamp=datetime.now().isoformat(),
    )


# Endpoint GET: Kthen CBOR
@router.get("/alba/cbor", response_class=Response)
async def get_cbor():
    data = {"status": "ok", "timestamp": "2025-10-09", "module": "alba"}
    cbor_bytes = cbor2.dumps(data)
    return Response(content=cbor_bytes, media_type="application/cbor")


# Endpoint POST: Pranon CBOR
@router.post("/alba/cbor", response_class=Response)
async def post_cbor(request: Request):
    body = await request.body()
    if not body:
        payload = {
            "received": False,
            "error": "Empty CBOR payload",
            "timestamp": datetime.now().isoformat(),
        }
        return Response(
            content=cbor2.dumps(payload), media_type="application/cbor"
        )

    try:
        data = cbor2.loads(body)
        response = {
            "received": True,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }
        return Response(
            content=cbor2.dumps(response), media_type="application/cbor"
        )
    except Exception as e:
        error = {
            "received": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat(),
        }
        return Response(
            content=cbor2.dumps(error),
            media_type="application/cbor",
            status_code=400
        )


@router.post("/streams/start", response_model=StreamStartResponse)
async def start_data_stream(
    stream_config: StreamStartRequest,
) -> StreamStartResponse:
    """Start a new data collection stream"""
    stream_id = stream_config.stream_id or f"stream_{len(active_streams) + 1}"

    active_streams[stream_id] = {
        "config": stream_config.dict(exclude_none=True),
        "start_time": datetime.now(),
        "data_points": 0,
        "status": "active",
    }

    return StreamStartResponse(
        message=f"Stream {stream_id} started successfully",
        stream_id=stream_id,
        status="active",
    )


@router.post("/streams/{stream_id}/stop", response_model=StreamStopResponse)
async def stop_data_stream(stream_id: str) -> StreamStopResponse:
    """Stop a data collection stream"""
    if stream_id not in active_streams:
        raise HTTPException(status_code=404, detail="Stream not found")
    
    active_streams[stream_id]["status"] = "stopped"
    active_streams[stream_id]["end_time"] = datetime.now()

    return StreamStopResponse(
        message=f"Stream {stream_id} stopped",
        stream_id=stream_id,
        status="stopped",
    )


def _serialize_streams() -> Dict[str, StreamInfo]:
    serialized: Dict[str, StreamInfo] = {}
    for sid, payload in active_streams.items():
        start_time = payload.get("start_time")
        end_time = payload.get("end_time")
        serialized[sid] = StreamInfo(
            config=payload.get("config", {}),
            start_time=(
                start_time.isoformat()
                if isinstance(start_time, datetime)
                else str(start_time)
            ),
            data_points=payload.get("data_points", 0),
            status=payload.get("status", "unknown"),
            end_time=(
                end_time.isoformat()
                if isinstance(end_time, datetime)
                else None
            ),
        )
    return serialized


@router.get("/streams", response_model=StreamsOverview)
async def get_active_streams() -> StreamsOverview:
    """Get all active data streams"""
    return StreamsOverview(
        active_streams=_serialize_streams(), total_streams=len(active_streams)
    )


@router.get("/streams/{stream_id}/data", response_model=StreamDataResponse)
async def get_stream_data(
    stream_id: str, limit: int = 100
) -> StreamDataResponse:
    """Get collected data from specific stream"""
    if stream_id not in active_streams:
        raise HTTPException(status_code=404, detail="Stream not found")
    
    # Simulated EEG data
    simulated_data = {
        "stream_id": stream_id,
        "data_points": [
            {
                "timestamp": datetime.now().isoformat(),
                "channel_1": 0.5 + 0.1 * i,
                "channel_2": 0.3 + 0.05 * i,
                "channel_3": 0.7 + 0.02 * i,
                "signal_quality": 0.95 - 0.01 * i
            }
            for i in range(min(limit, 50))
        ],
        "metadata": active_streams[stream_id]
    }
    
    stream_info = _serialize_streams().get(stream_id)
    if not stream_info:
        raise HTTPException(
            status_code=404,
            detail="Stream info could not be serialized"
        )

    data_points_list: List[StreamDataPoint] = []
    points_data: List[Dict[str, Any]] = list(simulated_data.get(
        "data_points", []
    ))
    for point in points_data:
        data_points_list.append(
            StreamDataPoint(
                timestamp=point.get("timestamp", ""),
                channel_1=float(point.get("channel_1", 0.0)),
                channel_2=float(point.get("channel_2", 0.0)),
                channel_3=float(point.get("channel_3", 0.0)),
                signal_quality=float(point.get("signal_quality", 0.0)),
            )
        )

    return StreamDataResponse(
        stream_id=stream_id,
        data_points=data_points_list,
        metadata=active_streams.get(stream_id, {}),
    )


@router.websocket("/ws/{stream_id}")
async def websocket_data_stream(websocket: WebSocket, stream_id: str):
    """WebSocket for real-time EEG data streaming"""
    await websocket.accept()
    
    try:
        while True:
            # Simulate real-time EEG data
            eeg_data = {
                "stream_id": stream_id,
                "timestamp": datetime.now().isoformat(),
                "channels": {
                    f"channel_{i}": 0.5 + 0.1 * (i % 8) for i in range(8)
                },
                "frequency_bands": {
                    "delta": 0.1 + 0.05 * (datetime.now().second % 10),
                    "theta": 0.2 + 0.08 * (datetime.now().second % 10),
                    "alpha": 0.3 + 0.12 * (datetime.now().second % 10),
                    "beta": 0.4 + 0.15 * (datetime.now().second % 10),
                    "gamma": 0.5 + 0.18 * (datetime.now().second % 10)
                },
                "signal_quality": 0.95
            }
            
            await websocket.send_json(eeg_data)
            await asyncio.sleep(0.1)  # 10Hz data rate
            
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for stream {stream_id}")


@router.post("/config", response_model=CollectionConfigResponse)
async def update_collection_config(
    config: CollectionConfigUpdate,
) -> CollectionConfigResponse:
    """Update data collection configuration"""
    global stream_configs
    payload = config.dict(exclude_none=True)
    settings_payload = payload.pop("settings", {})
    stream_configs.update(settings_payload)
    if payload:
        stream_configs.update(payload)

    return CollectionConfigResponse(
        message="Configuration updated", new_config=stream_configs
    )


@router.get("/metrics", response_model=CollectionMetrics)
async def get_collection_metrics() -> CollectionMetrics:
    """Get data collection metrics"""
    total_data_points = sum(
        stream["data_points"] for stream in active_streams.values()
    )
    active_streams_count = len(
        [s for s in active_streams.values() if s["status"] == "active"]
    )

    return CollectionMetrics(
        total_data_points=total_data_points,
        active_streams=active_streams_count,
        total_streams=len(active_streams),
        data_rate_Hz=256,
        storage_usage_mb=total_data_points * 0.001,
        uptime_hours=24,
    )


@router.get("/health", response_model=AlbaHealth)
async def health_check() -> AlbaHealth:
    """Health check endpoint"""
    return AlbaHealth(
        module="ALBA",
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.2.3",
    )

