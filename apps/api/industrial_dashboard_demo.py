from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional
import time


router = APIRouter()


class DataSource(BaseModel):
    name: str
    status: str
    records: int
    size_gb: float
    throughput: str
    location: str
    health: int
    uptime: float
    error_rate: float
    last_updated: str
    state: str


class ActivityLogEntry(BaseModel):
    time: str
    type: str
    source: str
    message: str


class BulkCollectionRequest(BaseModel):
    dataset: str = Field(..., description="Dataset identifier to collect")
    priority: str = Field("normal", pattern=r"^(low|normal|high)$")
    retention_hours: int = Field(24, ge=1, le=720)
    notes: Optional[str] = None


class BulkCollectionResponse(BaseModel):
    success: bool
    message: str
    collection_id: str
    started_at: float


class PerformanceMetrics(BaseModel):
    cpu_usage: float
    storage_used_tb: float
    storage_total_tb: float
    storage_percent: float
    network_throughput: float
    network_percent: float
    error_rate: float
    system_load: float
    connections: int
    data_rate: float


class SystemStatus(BaseModel):
    core_services: str
    network: str
    maintenance: str
    data_integrity: str


class SimpleAlert(BaseModel):
    active: bool
    message: str


@router.get("/api/data-sources", response_model=List[DataSource])
def get_data_sources() -> List[DataSource]:
    return [
        DataSource(
            name="EEG Neural Monitor Array",
            status="critical",
            records=154404,
            size_gb=23.4,
            throughput="2.4 MB/s",
            location="Lab Station A-1",
            health=98,
            uptime=99.97,
            error_rate=0.3,
            last_updated="just now",
            state="active",
        ),
        DataSource(
            name="Industrial Audio Processor",
            status="high",
            records=89760,
            size_gb=18.7,
            throughput="1.8 MB/s",
            location="Production Floor B-2",
            health=95,
            uptime=99.95,
            error_rate=0.5,
            last_updated="5 seconds ago",
            state="active",
        ),
        DataSource(
            name="Neural Pattern Recognition Engine",
            status="critical",
            records=235984,
            size_gb=42.1,
            throughput="3.2 MB/s",
            location="AI Processing Center",
            health=99,
            uptime=99.99,
            error_rate=0.1,
            last_updated="4 seconds ago",
            state="collecting",
        ),
        DataSource(
            name="Environmental Sensor Network",
            status="medium",
            records=54320,
            size_gb=8.9,
            throughput="512 KB/s",
            location="Facility Wide",
            health=92,
            uptime=99.85,
            error_rate=1.5,
            last_updated="10 seconds ago",
            state="active",
        ),
        DataSource(
            name="High-Frequency Audio Spectrometer",
            status="high",
            records=12340,
            size_gb=2.1,
            throughput="0 MB/s",
            location="Lab Station C-3",
            health=45,
            uptime=97.12,
            error_rate=28.5,
            last_updated="2 minutes ago",
            state="error",
        ),
        DataSource(
            name="Industrial Vibration Sensors",
            status="medium",
            records=78560,
            size_gb=12.3,
            throughput="0 MB/s",
            location="Machine Shop D-1",
            health=0,
            uptime=95.67,
            error_rate=0.0,
            last_updated="1 hour ago",
            state="maintenance",
        ),
    ]


@router.get("/api/activity-log", response_model=List[ActivityLogEntry])
def get_activity_log() -> List[ActivityLogEntry]:
    return [
        ActivityLogEntry(time="13:03:33", type="Collection", source="System Controller", message="Bulk data collection initiated successfully"),
        ActivityLogEntry(time="13:02:53", type="Detection", source="Neural Pattern Engine", message="High-frequency pattern detected in sector 7"),
        ActivityLogEntry(time="13:02:48", type="Network", source="Audio Spectrometer", message="Connection timeout - attempting reconnection"),
        ActivityLogEntry(time="13:02:41", type="Backup", source="EEG Monitor Array", message="Data backup completed successfully"),
        ActivityLogEntry(time="13:02:35", type="Storage", source="System Controller", message="Storage usage exceeded 75% threshold"),
    ]


@router.post("/api/start-bulk-collection", response_model=BulkCollectionResponse)
def start_bulk_collection(payload: BulkCollectionRequest) -> BulkCollectionResponse:
    time.sleep(1)
    collection_id = f"bulk-{int(time.time())}"
    return BulkCollectionResponse(
        success=True,
        message="Bulk data collection initiated successfully",
        collection_id=collection_id,
        started_at=time.time(),
    )


@router.get("/api/performance-metrics", response_model=PerformanceMetrics)
def get_performance_metrics() -> PerformanceMetrics:
    return PerformanceMetrics(
        cpu_usage=72.9,
        storage_used_tb=1.8,
        storage_total_tb=2.4,
        storage_percent=75.0,
        network_throughput=45.2,
        network_percent=60.0,
        error_rate=0.12,
        system_load=72.9,
        connections=19,
        data_rate=8.4,
    )


@router.get("/api/system-status", response_model=SystemStatus)
def get_system_status() -> SystemStatus:
    return SystemStatus(
        core_services="Operational",
        network="Connected",
        maintenance="Scheduled",
        data_integrity="Verified",
    )


@router.get("/api/storage-alert", response_model=SimpleAlert)
def get_storage_alert() -> SimpleAlert:
    return SimpleAlert(
        active=True,
        message="Storage usage has exceeded 75% capacity. Consider archiving older data.",
    )


@router.get("/api/audio-spectrometer-error", response_model=SimpleAlert)
def get_audio_spectrometer_error() -> SimpleAlert:
    return SimpleAlert(
        active=True,
        message="Audio Spectrometer connection failed. Check network configuration.",
    )
