"""
ULTRA REPORTING API ENDPOINTS
Automat raportet: Excel + PowerPoint + Dashboards në kërkesë
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Query, Request
from fastapi.responses import JSONResponse, PlainTextResponse, Response
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Dict, Any, List
import os
import sys
import logging
from pathlib import Path
import json

try:
    import cbor2  # type: ignore
except ImportError:  # pragma: no cover - runtime safety
    cbor2 = None

try:
    import msgpack  # type: ignore
except ImportError:  # pragma: no cover - runtime safety
    msgpack = None

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import the ultra reporting module
from ultra_reporting import (
    UltraExcelExporter,
    UltraPowerPointGenerator,
    UltraReportGenerator,
    MetricsSnapshot
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/reporting", tags=["reporting"])

# Ensure reports directory exists
REPORTS_DIR = Path("./reports")
REPORTS_DIR.mkdir(exist_ok=True)


class ExportRequest(BaseModel):
    """Request body për Excel/PowerPoint export"""
    title: str = "Clisonix Cloud Metrics Report"
    format: str = "xlsx"  # xlsx, pptx, both
    include_sla: bool = True
    include_alerts: bool = True
    date_range_hours: int = 24


class ReportMetadata(BaseModel):
    """Metadata për raportin e gjeneruar"""
    id: str
    title: str
    format: str
    generated_at: str
    file_path: str
    size_bytes: int


class DashboardMetrics(BaseModel):
    """Unified dashboard metrics"""
    api_uptime_percent: float
    api_requests_per_second: int
    api_error_rate_percent: float
    api_latency_p95_ms: float
    api_latency_p99_ms: float
    ai_agent_calls_24h: int
    ai_agent_success_rate: float
    documents_generated_24h: int
    cache_hit_rate_percent: float
    system_cpu_percent: float
    system_memory_percent: float
    system_disk_percent: float
    active_alerts: List[Dict[str, Any]]
    sla_status: str


LIGHTWEIGHT_MIME_MAP = {
    "cbor": "application/cbor",
    "msgpack": "application/msgpack",
    "compact": "text/plain",
    "lora": "text/plain",
}


def _pick_format(request: Request) -> str:
    format_param = (request.query_params.get("format") or "").strip().lower()
    if format_param in {"json", "cbor", "msgpack", "mpack", "mpk", "compact", "lora", "minimal"}:
        return format_param

    accept = (request.headers.get("accept") or "").lower()
    if "application/cbor" in accept:
        return "cbor"
    if "application/msgpack" in accept or "application/x-msgpack" in accept:
        return "msgpack"
    if "text/plain" in accept and "json" not in accept:
        return "compact"
    return "json"


def _format_numeric(value: Any) -> Any:
    if isinstance(value, float):
        return round(value, 3)
    return value


def _as_compact(payload: Dict[str, Any], mode: str) -> str:
    if "api_uptime_percent" not in payload:
        # Generic fallback for broader payloads (e.g., history, stats)
        flat: Dict[str, Any] = {}
        for key, value in payload.items():
            if isinstance(value, (int, float, str)):
                flat[key] = _format_numeric(value)
        if mode in {"lora", "minimal"}:
            if flat:
                return "|".join(f"{key}={value}" for key, value in flat.items())
            return json.dumps(payload, separators=(",", ":"))
        if flat:
            return json.dumps(flat, separators=(",", ":"))
        return json.dumps(payload, separators=(",", ":"))

    essentials = {
        "upt": _format_numeric(payload.get("api_uptime_percent")),
        "reqps": _format_numeric(payload.get("api_requests_per_second")),
        "err": _format_numeric(payload.get("api_error_rate_percent")),
        "lat95": _format_numeric(payload.get("api_latency_p95_ms")),
        "lat99": _format_numeric(payload.get("api_latency_p99_ms")),
        "ai": _format_numeric(payload.get("ai_agent_calls_24h")),
        "ai_ok": _format_numeric(payload.get("ai_agent_success_rate")),
        "doc24": _format_numeric(payload.get("documents_generated_24h")),
        "cache": _format_numeric(payload.get("cache_hit_rate_percent")),
        "cpu": _format_numeric(payload.get("system_cpu_percent")),
        "mem": _format_numeric(payload.get("system_memory_percent")),
        "disk": _format_numeric(payload.get("system_disk_percent")),
        "alerts": len(payload.get("active_alerts", [])),
        "sla": payload.get("sla_status"),
    }

    if mode in {"lora", "minimal"}:
        return "|".join(f"{key}={value}" for key, value in essentials.items() if value is not None)

    return json.dumps({k: v for k, v in essentials.items() if v is not None}, separators=(",", ":"))


def _serialize_payload(request: Request, payload: Dict[str, Any]) -> Response:
    fmt = _pick_format(request)

    if fmt == "json" or fmt == "":
        return JSONResponse(payload)

    if fmt == "cbor":
        if cbor2 is None:
            raise HTTPException(status_code=406, detail="CBOR format unavailable - install cbor2")
        return Response(content=cbor2.dumps(payload), media_type=LIGHTWEIGHT_MIME_MAP["cbor"])

    if fmt in {"msgpack", "mpack", "mpk"}:
        if msgpack is None:
            raise HTTPException(status_code=406, detail="MessagePack format unavailable - install msgpack")
        return Response(content=msgpack.packb(payload, use_bin_type=True), media_type=LIGHTWEIGHT_MIME_MAP["msgpack"])

    if fmt in {"compact", "lora", "minimal"}:
        text_payload = _as_compact(payload, fmt)
        return PlainTextResponse(text_payload, media_type=LIGHTWEIGHT_MIME_MAP.get(fmt, "text/plain"))

    # Fallback to JSON for any unknown request
    return JSONResponse(payload)


@router.post("/export-excel")
async def export_excel(request: ExportRequest, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """
    Eksporto metriken në Excel me grafike, pivot tabela, dhe SLA tracking
    
    Returns:
        - file_path: Stegu i file-it të gjeneruar
        - download_url: URL për download-imin
    """
    try:
        # Generate Excel file
        excel_exporter = UltraExcelExporter(request.title)
        
        # Fetch mock metrics (in real implementation, query VictoriaMetrics)
        snapshots = _get_mock_metrics(hours=request.date_range_hours)
        excel_exporter.add_metrics(snapshots)
        
        # Save file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"metrics_report_{timestamp}.xlsx"
        filepath = REPORTS_DIR / filename
        
        excel_exporter.save(str(filepath))
        
        file_size = filepath.stat().st_size
        
        return {
            "success": True,
            "file_path": str(filepath),
            "filename": filename,
            "size_bytes": file_size,
            "download_url": f"/api/reporting/download/{filename}",
            "generated_at": datetime.now().isoformat(),
            "message": f"✓ Excel report generated successfully: {filename}"
        }
        
    except Exception as e:
        logger.error(f"Excel export failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate Excel report: {str(e)}"
        )


@router.post("/export-pptx")
async def export_powerpoint(request: ExportRequest, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """
    Eksporto metriken në PowerPoint presentation
    
    Includes:
    - Title slide
    - Metrics summary
    - SLA status
    - Active alerts
    - Trend analysis
    """
    try:
        # Generate PowerPoint
        ppt_gen = UltraPowerPointGenerator(request.title)
        
        # Add slides
        ppt_gen.add_title_slide("Enterprise Metrics & SLA Tracking Report")
        
        metrics = {
            "api_uptime": "99.9%",
            "avg_latency": "87ms",
            "error_rate": "0.12%",
            "docs_per_day": "2,400"
        }
        ppt_gen.add_metrics_slide(metrics)
        
        if request.include_sla:
            ppt_gen.add_sla_slide()
            
        if request.include_alerts:
            alerts = [
                {"severity": "INFO", "message": "High request volume", "timestamp": "2 min ago"},
                {"severity": "WARNING", "message": "Memory usage above 70%", "timestamp": "5 min ago"},
            ]
            ppt_gen.add_alerts_slide(alerts)
        
        # Save file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"metrics_presentation_{timestamp}.pptx"
        filepath = REPORTS_DIR / filename
        
        ppt_gen.save(str(filepath))
        
        file_size = filepath.stat().st_size
        
        return {
            "success": True,
            "file_path": str(filepath),
            "filename": filename,
            "size_bytes": file_size,
            "download_url": f"/api/reporting/download/{filename}",
            "generated_at": datetime.now().isoformat(),
            "message": f"✓ PowerPoint presentation generated: {filename}"
        }
        
    except Exception as e:
        logger.error(f"PowerPoint export failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate PowerPoint: {str(e)}"
        )


@router.post("/export-both")
async def export_both(request: ExportRequest) -> Dict[str, Any]:
    """Eksporto si Excel edhe PowerPoint në të njejtën kohë"""
    
    try:
        # Generate Excel
        excel_exporter = UltraExcelExporter(request.title)
        snapshots = _get_mock_metrics(hours=request.date_range_hours)
        excel_exporter.add_metrics(snapshots)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        excel_filename = f"metrics_report_{timestamp}.xlsx"
        excel_filepath = REPORTS_DIR / excel_filename
        excel_exporter.save(str(excel_filepath))
        
        # Generate PowerPoint
        ppt_gen = UltraPowerPointGenerator(request.title)
        ppt_gen.add_title_slide("Enterprise Metrics & SLA Tracking")
        ppt_gen.add_metrics_slide({
            "api_uptime": "99.9%",
            "avg_latency": "87ms",
            "error_rate": "0.12%",
            "docs_per_day": "2,400"
        })
        
        if request.include_sla:
            ppt_gen.add_sla_slide()
        if request.include_alerts:
            ppt_gen.add_alerts_slide([])
            
        ppt_filename = f"metrics_presentation_{timestamp}.pptx"
        ppt_filepath = REPORTS_DIR / ppt_filename
        ppt_gen.save(str(ppt_filepath))
        
        return {
            "success": True,
            "reports": {
                "excel": {
                    "filename": excel_filename,
                    "file_path": str(excel_filepath),
                    "download_url": f"/api/reporting/download/{excel_filename}",
                    "size_bytes": excel_filepath.stat().st_size
                },
                "powerpoint": {
                    "filename": ppt_filename,
                    "file_path": str(ppt_filepath),
                    "download_url": f"/api/reporting/download/{ppt_filename}",
                    "size_bytes": ppt_filepath.stat().st_size
                }
            },
            "generated_at": datetime.now().isoformat(),
            "message": "✓ Both Excel and PowerPoint reports generated successfully"
        }
        
    except Exception as e:
        logger.error(f"Export both failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard")
async def get_unified_dashboard(request: Request) -> Response:
    """
    Unified dashboard combining Datadog + Grafana + Prometheus metrics
    
    Real implementation would:
    - Query VictoriaMetrics for latest metrics
    - Fetch from Prometheus for detailed data
    - Get alerts from AlertManager
    - Aggregate all sources into single response
    """
    
    try:
        metrics = DashboardMetrics(
            api_uptime_percent=99.87,
            api_requests_per_second=4850,
            api_error_rate_percent=0.12,
            api_latency_p95_ms=87.4,
            api_latency_p99_ms=145.2,
            ai_agent_calls_24h=125600,
            ai_agent_success_rate=99.43,
            documents_generated_24h=2400,
            cache_hit_rate_percent=92.1,
            system_cpu_percent=35.5,
            system_memory_percent=62.3,
            system_disk_percent=45.1,
            active_alerts=[
                {
                    "severity": "INFO",
                    "name": "HighRequestVolume",
                    "message": "API request volume above 4000 req/s",
                    "fired_at": (datetime.now() - timedelta(minutes=2)).isoformat(),
                    "value": 4850
                },
                {
                    "severity": "WARNING",
                    "name": "MemoryUsageHigh",
                    "message": "System memory usage above 60%",
                    "fired_at": (datetime.now() - timedelta(minutes=5)).isoformat(),
                    "value": 62.3
                }
            ],
            sla_status="✓ ALL PASSED"
        )
        payload = metrics.model_dump() if hasattr(metrics, "model_dump") else metrics.dict()
        return _serialize_payload(request, payload)

    except Exception as e:
        logger.error(f"Dashboard fetch failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics-history")
async def get_metrics_history(
    request: Request,
    hours: int = Query(24, ge=1, le=720),
    metric_type: str = Query("all", regex="^(all|api|ai|infrastructure)$")
) -> Response:
    """
    Merr historiken e metrikave për periudhën e caktuar
    
    Metric types:
    - all: Të gjitha metriken
    - api: API request/error/latency metrics
    - ai: AI agent metrics
    - infrastructure: System/DB/cache metrics
    """
    
    try:
        snapshots = _get_mock_metrics(hours=hours)
        
        history = {
            "period_hours": hours,
            "data_points": len(snapshots),
            "metrics": {
                "api_requests": [s.api_requests_total for s in snapshots],
                "error_rate": [s.api_error_rate * 100 for s in snapshots],
                "latency_p95": [s.api_latency_p95 for s in snapshots],
                "latency_p99": [s.api_latency_p99 for s in snapshots],
                "ai_calls": [s.ai_agent_calls for s in snapshots],
                "documents_generated": [s.documents_generated for s in snapshots],
                "cache_hit_rate": [s.cache_hit_rate * 100 for s in snapshots],
                "cpu_percent": [s.system_cpu_percent for s in snapshots],
                "memory_percent": [s.system_memory_percent for s in snapshots],
            },
            "timestamps": [s.timestamp.isoformat() for s in snapshots],
            "generated_at": datetime.now().isoformat()
        }
        
        return _serialize_payload(request, history)
        
    except Exception as e:
        logger.error(f"Metrics history fetch failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/download/{filename}")
async def download_report(filename: str):
    """Shkarko raportin e gjeneruar"""
    
    from fastapi.responses import FileResponse
    
    try:
        filepath = REPORTS_DIR / filename
        
        if not filepath.exists():
            raise HTTPException(status_code=404, detail="Report not found")
            
        return FileResponse(
            path=filepath,
            media_type="application/octet-stream",
            filename=filename
        )
        
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/list-reports")
async def list_reports() -> List[ReportMetadata]:
    """Listo të gjithë raportet e gjeneruar"""
    
    try:
        reports = []
        
        for filepath in REPORTS_DIR.glob("*"):
            if filepath.is_file():
                stat = filepath.stat()
                
                reports.append(ReportMetadata(
                    id=filepath.stem,
                    title=filepath.stem.replace("_", " "),
                    format=filepath.suffix.lower().lstrip("."),
                    generated_at=datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    file_path=str(filepath),
                    size_bytes=stat.st_size
                ))
                
        return sorted(reports, key=lambda r: r.generated_at, reverse=True)
        
    except Exception as e:
        logger.error(f"List reports failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear-reports")
async def clear_old_reports(days_old: int = Query(7, ge=1)) -> Dict[str, Any]:
    """Pastro raportet e vjetra më shumë se N ditë"""
    
    try:
        cutoff_time = datetime.now() - timedelta(days=days_old)
        deleted_count = 0
        total_freed = 0
        
        for filepath in REPORTS_DIR.glob("*"):
            if filepath.is_file():
                file_time = datetime.fromtimestamp(filepath.stat().st_mtime)
                if file_time < cutoff_time:
                    size = filepath.stat().st_size
                    filepath.unlink()
                    deleted_count += 1
                    total_freed += size
                    
        return {
            "success": True,
            "deleted_files": deleted_count,
            "freed_bytes": total_freed,
            "freed_mb": round(total_freed / (1024 * 1024), 2),
            "message": f"✓ Deleted {deleted_count} reports older than {days_old} days"
        }
        
    except Exception as e:
        logger.error(f"Clear reports failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def _get_mock_metrics(hours: int = 24) -> List[MetricsSnapshot]:
    """Generate mock metrics for demonstration"""
    
    snapshots = []
    now = datetime.now()
    
    for i in range(hours):
        snapshots.append(MetricsSnapshot(
            timestamp=now - timedelta(hours=i),
            api_requests_total=5000 + i * 50,
            api_error_rate=0.001 + (i % 3) * 0.0001,
            api_latency_p95=85 + (i % 10) * 2,
            api_latency_p99=140 + (i % 10) * 3,
            ai_agent_calls=500 + i * 10,
            ai_agent_errors=max(0, (i // 5) - 1),
            documents_generated=95 + (i % 15) * 3,
            documents_failed=0 if i % 20 != 0 else 1,
            cache_hit_rate=0.92 - (i % 5) * 0.01,
            db_connections=40 + (i % 10),
            system_cpu_percent=30 + (i % 20) * 0.5,
            system_memory_percent=60 + (i % 10) * 0.2,
            system_disk_percent=45.0
        ))
        
    return sorted(snapshots, key=lambda s: s.timestamp)
