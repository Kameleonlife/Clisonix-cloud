"""
Agent Telemetry Integration
Connects AI agents (AGIEM, ASI, Blerina) to Alba/Albi/Jona telemetry pipeline
"""

import json
import time
import logging
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from dataclasses import dataclass, asdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgentTelemetry")


@dataclass
class AgentMetrics:
    """Standardized metrics structure for AI agents"""
    agent_name: str
    timestamp: float
    status: str
    operation: str
    duration_ms: Optional[float] = None
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    success: bool = True
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class TelemetryRouter:
    """Routes agent telemetry to Alba/Albi/Jona based on data type"""
    
    def __init__(
        self,
        alba_url: str = "http://localhost:5050",
        albi_url: str = "http://localhost:6060",
        jona_url: str = "http://localhost:7070",
        enabled: bool = True
    ):
        self.alba_url = alba_url
        self.albi_url = albi_url
        self.jona_url = jona_url
        self.enabled = enabled
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        
        logger.info(f"TelemetryRouter initialized (enabled={enabled})")
        logger.info(f"  Alba: {alba_url}")
        logger.info(f"  Albi: {albi_url}")
        logger.info(f"  Jona: {jona_url}")
    
    def send_to_alba(self, metrics: AgentMetrics) -> bool:
        """Send raw data collection metrics to Alba"""
        if not self.enabled:
            return True
            
        try:
            payload = {
                "source": metrics.agent_name,
                "timestamp": metrics.timestamp,
                "type": "agent_telemetry",
                "data": asdict(metrics)
            }
            
            response = self.session.post(
                f"{self.alba_url}/api/telemetry/ingest",
                json=payload,
                timeout=5
            )
            
            if response.status_code in [200, 201]:
                logger.debug(f"✓ Alba: {metrics.agent_name} telemetry sent")
                return True
            else:
                logger.warning(f"Alba returned {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Alba send failed: {e}")
            return False
    
    def send_to_albi(self, metrics: AgentMetrics) -> bool:
        """Send processing/analytics metrics to Albi"""
        if not self.enabled:
            return True
            
        try:
            payload = {
                "agent": metrics.agent_name,
                "timestamp": metrics.timestamp,
                "operation": metrics.operation,
                "duration_ms": metrics.duration_ms,
                "tokens": {
                    "input": metrics.input_tokens,
                    "output": metrics.output_tokens
                },
                "success": metrics.success,
                "metadata": metrics.metadata or {}
            }
            
            response = self.session.post(
                f"{self.albi_url}/api/analytics/agent",
                json=payload,
                timeout=5
            )
            
            if response.status_code in [200, 201]:
                logger.debug(f"✓ Albi: {metrics.agent_name} analytics sent")
                return True
            else:
                logger.warning(f"Albi returned {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Albi send failed: {e}")
            return False
    
    def send_to_jona(self, metrics: AgentMetrics) -> bool:
        """Send coordination/orchestration metrics to Jona"""
        if not self.enabled:
            return True
            
        try:
            payload = {
                "agent": metrics.agent_name,
                "timestamp": metrics.timestamp,
                "status": metrics.status,
                "operation": metrics.operation,
                "success": metrics.success,
                "error": metrics.error
            }
            
            response = self.session.post(
                f"{self.jona_url}/api/coordination/event",
                json=payload,
                timeout=5
            )
            
            if response.status_code in [200, 201]:
                logger.debug(f"✓ Jona: {metrics.agent_name} event sent")
                return True
            else:
                logger.warning(f"Jona returned {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Jona send failed: {e}")
            return False
    
    def send_all(self, metrics: AgentMetrics) -> Dict[str, bool]:
        """Send metrics to all three services"""
        results = {
            "alba": self.send_to_alba(metrics),
            "albi": self.send_to_albi(metrics),
            "jona": self.send_to_jona(metrics)
        }
        
        success_count = sum(results.values())
        logger.info(
            f"📊 {metrics.agent_name}.{metrics.operation}: "
            f"{success_count}/3 telemetry endpoints reached"
        )
        
        return results


class AgentTelemetryMixin:
    """Mixin class for AI agents to add telemetry capabilities"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.telemetry = TelemetryRouter(
            enabled=kwargs.get("telemetry_enabled", True)
        )
        self._operation_start: Optional[float] = None
    
    def start_operation(self, operation_name: str):
        """Mark the start of an operation for timing"""
        self._operation_start = time.time()
        self._current_operation = operation_name
    
    def end_operation(
        self,
        success: bool = True,
        error: Optional[str] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Mark the end of an operation and send telemetry"""
        if self._operation_start is None:
            logger.warning("end_operation called without start_operation")
            return
        
        duration_ms = (time.time() - self._operation_start) * 1000
        
        metrics = AgentMetrics(
            agent_name=getattr(self, "agent_name", self.__class__.__name__),
            timestamp=time.time(),
            status="success" if success else "error",
            operation=self._current_operation,
            duration_ms=duration_ms,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            success=success,
            error=error,
            metadata=metadata
        )
        
        self.telemetry.send_all(metrics)
        self._operation_start = None


# Standalone telemetry sender for scripts
_global_router: Optional[TelemetryRouter] = None


def init_telemetry(
    alba_url: str = "http://localhost:5050",
    albi_url: str = "http://localhost:6060",
    jona_url: str = "http://localhost:7070",
    enabled: bool = True
):
    """Initialize global telemetry router"""
    global _global_router
    _global_router = TelemetryRouter(alba_url, albi_url, jona_url, enabled)
    return _global_router


def send_agent_telemetry(
    agent_name: str,
    operation: str,
    duration_ms: Optional[float] = None,
    success: bool = True,
    error: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
):
    """Send telemetry using global router"""
    if _global_router is None:
        init_telemetry()
    
    metrics = AgentMetrics(
        agent_name=agent_name,
        timestamp=time.time(),
        status="success" if success else "error",
        operation=operation,
        duration_ms=duration_ms,
        success=success,
        error=error,
        metadata=metadata
    )
    
    return _global_router.send_all(metrics)


if __name__ == "__main__":
    # Test telemetry integration
    print("🧪 Testing Agent Telemetry Integration\n")
    
    router = TelemetryRouter()
    
    # Test AGIEM telemetry
    agiem_metrics = AgentMetrics(
        agent_name="AGIEM",
        timestamp=time.time(),
        status="success",
        operation="pipeline_execution",
        duration_ms=1234.56,
        input_tokens=500,
        output_tokens=150,
        success=True,
        metadata={"stage": "data_collection", "nodes": 3}
    )
    
    print("Testing AGIEM -> Alba/Albi/Jona...")
    results = router.send_all(agiem_metrics)
    print(f"Results: {results}\n")
    
    # Test ASI telemetry
    asi_metrics = AgentMetrics(
        agent_name="ASI",
        timestamp=time.time(),
        status="success",
        operation="realtime_analysis",
        duration_ms=567.89,
        success=True,
        metadata={"nodes": ["ALBA", "ALBI", "JONA"], "health_score": 0.95}
    )
    
    print("Testing ASI -> Alba/Albi/Jona...")
    results = router.send_all(asi_metrics)
    print(f"Results: {results}\n")
    
    # Test Blerina telemetry
    blerina_metrics = AgentMetrics(
        agent_name="Blerina",
        timestamp=time.time(),
        status="success",
        operation="youtube_metadata_extraction",
        duration_ms=234.12,
        success=True,
        metadata={"video_id": "dQw4w9WgXcQ", "views": 1721885158}
    )
    
    print("Testing Blerina -> Alba/Albi/Jona...")
    results = router.send_all(blerina_metrics)
    print(f"Results: {results}\n")
    
    print("✅ Telemetry integration test complete")
