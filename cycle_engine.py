# -*- coding: utf-8 -*-
"""
🔁 CYCLE ENGINE – Inteligjenca kontraktore e sistemit
=====================================================
Krijon, menaxhon dhe ekzekuton cycles (kontrata pune inteligjente)
të lidhura me source, domain, agent, alignment dhe policy.

Çdo cycle:
- Ka burim (ALBA stream, PubMed, FIWARE, etj)
- Ekzekuton një detyrë (ingest, analyze, monitor)
- Respekton alignment (JONA oversight)
- Auto-evolon (Born-Concepts për gaps)
"""

from __future__ import annotations
import asyncio
import json
import uuid
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Literal
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

try:
    from alba_core import AlbaCore
except:
    AlbaCore = None

try:
    from albi_core import AlbiCore
except:
    AlbiCore = None

try:
    from jona_character import get_jona
except:
    get_jona = None


class CycleType(Enum):
    """Llojet e cycles"""
    INTERVAL = "interval"          # Periodic (çdo N sekonda)
    EVENT = "event"                # Trigger-based (kur ndodh X)
    BATCH = "batch"                # One-time (një herë)
    STREAM = "stream"              # Continuous (pa pushim)
    ADAPTIVE = "adaptive"          # Auto-adjust (vetë-rregullohet)
    GAP_TRIGGERED = "gap_triggered" # Kur mungon kuptimi


class CycleStatus(Enum):
    """Gjendjet e një cycle"""
    PENDING = "pending"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"            # JONA e ka bllokuar
    HUMAN_REVIEW = "human_review"  # Kërkon njeri


class AlignmentPolicy(Enum):
    """Politikat e alignment"""
    STRICT = "strict"              # Çdo gabim ndal
    MODERATE = "moderate"          # Warning por vazhdon
    PERMISSIVE = "permissive"      # Vetëm log
    ETHICAL_GUARD = "ethical_guard" # JONA vendos


@dataclass
class CycleDefinition:
    """Përcaktimi i një cycle"""
    cycle_id: str = field(default_factory=lambda: f"cycle_{uuid.uuid4().hex[:8]}")
    domain: str = "general"
    source: Optional[str] = None
    agent: str = "ALBA"
    task: str = "monitor"
    cycle_type: CycleType = CycleType.INTERVAL
    interval: Optional[float] = None  # sekonda
    event_trigger: Optional[str] = None
    alignment: AlignmentPolicy = AlignmentPolicy.MODERATE
    target_storage: List[str] = field(default_factory=lambda: ["local"])
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    status: CycleStatus = CycleStatus.PENDING


@dataclass
class CycleExecution:
    """Rezultati i një ekzekutimi cycle"""
    cycle_id: str
    execution_id: str = field(default_factory=lambda: f"exec_{uuid.uuid4().hex[:8]}")
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    status: CycleStatus = CycleStatus.ACTIVE
    data_processed: int = 0
    insights_generated: int = 0
    gaps_detected: int = 0
    alignment_score: float = 1.0
    jona_review: Optional[str] = None
    error: Optional[str] = None
    output: Dict[str, Any] = field(default_factory=dict)


class CycleEngine:
    """
    🔁 Motori kryesor i Cycles
    
    Përgjegjësi:
    - Krijon cycles nga çdo domain
    - Ekzekuton cycles me agents (ALBA/ALBI/JONA)
    - Respekton alignment policies
    - Auto-krijon cycles për gaps (Born-Concepts)
    - Menaxhon event-based dhe streaming cycles
    """
    
    def __init__(self, data_root: Optional[Path] = None):
        self.data_root = Path(data_root) if data_root else Path.cwd() / "data"
        self.cycles: Dict[str, CycleDefinition] = {}
        self.executions: Dict[str, List[CycleExecution]] = {}
        self.active_tasks: Dict[str, asyncio.Task] = {}
        
        # Inicializo agents
        self.alba = AlbaCore(auto_start=False) if AlbaCore else None
        self.albi = AlbiCore() if AlbiCore else None
        self.jona = get_jona() if get_jona else None
        
        # Concept gaps queue (për Born-Concepts)
        self.concept_gaps: List[Dict[str, Any]] = []
        
        # Metrics
        self.metrics = {
            "total_cycles": 0,
            "active_cycles": 0,
            "completed_cycles": 0,
            "blocked_cycles": 0,
            "gaps_filled": 0
        }
    
    # ==================== CYCLE CREATION ====================
    
    def create_cycle(
        self,
        domain: str,
        source: Optional[str] = None,
        agent: str = "ALBA",
        task: str = "monitor",
        cycle_type: str = "interval",
        interval: Optional[float] = None,
        event_trigger: Optional[str] = None,
        alignment: str = "moderate",
        target: Optional[List[str]] = None,
        **kwargs
    ) -> CycleDefinition:
        """
        🔁 Krijon një cycle të ri
        
        Shembuj:
        
        # Neuro monitoring
        cycle = engine.create_cycle(
            domain="neuro",
            source="alba.eeg.stream",
            agent="ALBA",
            task="frequency_monitor",
            interval=1.0,
            alignment="strict"
        )
        
        # Open Data ingestion
        cycle = engine.create_cycle(
            domain="scientific",
            source="pubmed",
            task="literature_ingest",
            interval=86400,  # 24h
            target=["weaviate", "neo4j"],
            on_gap="born-concept"
        )
        
        # Event-based
        cycle = engine.create_cycle(
            domain="neuro",
            event_trigger="beta>25Hz",
            task="stress_alert",
            agent="JONA",
            alignment="ethical_guard"
        )
        """
        cycle_def = CycleDefinition(
            domain=domain,
            source=source,
            agent=agent,
            task=task,
            cycle_type=CycleType(cycle_type),
            interval=interval,
            event_trigger=event_trigger,
            alignment=AlignmentPolicy(alignment),
            target_storage=target or ["local"],
            metadata=kwargs
        )
        
        self.cycles[cycle_def.cycle_id] = cycle_def
        self.executions[cycle_def.cycle_id] = []
        self.metrics["total_cycles"] += 1
        
        print(f"✓ Cycle created: {cycle_def.cycle_id} ({domain}/{task})")
        return cycle_def
    
    def auto_create_cycles(
        self,
        trigger: str = "low_confidence",
        max_cycles: int = 10,
        domain: Optional[str] = None
    ) -> List[CycleDefinition]:
        """
        🤖 Auto-krijon cycles kur sistemi nuk kupton
        
        Trigger types:
        - low_confidence: Kur ALBI ka besim < 70%
        - concept_gap: Kur mungon një koncept në graph
        - anomaly_spike: Kur ka shumë anomali
        - data_stale: Kur data është e vjetër
        """
        created = []
        
        if trigger == "low_confidence" and self.albi:
            # Shikon nëse ALBI ka probleme
            gaps = self._detect_knowledge_gaps()
            for gap in gaps[:max_cycles]:
                cycle = self.create_cycle(
                    domain=domain or gap.get("domain", "general"),
                    source=gap.get("suggested_source"),
                    agent="ALBI",
                    task="gap_fill",
                    cycle_type="gap_triggered",
                    alignment="moderate",
                    gap_info=gap
                )
                created.append(cycle)
                self.concept_gaps.append(gap)
        
        elif trigger == "concept_gap":
            # Born-Concepts mode
            for gap in self.concept_gaps[:max_cycles]:
                cycle = self.create_cycle(
                    domain=gap.get("domain", "unknown"),
                    source="born_concepts",
                    agent="ALBI",
                    task="concept_birth",
                    cycle_type="gap_triggered",
                    concept=gap.get("missing_concept")
                )
                created.append(cycle)
        
        print(f"🤖 Auto-created {len(created)} cycles for {trigger}")
        return created
    
    def _detect_knowledge_gaps(self) -> List[Dict[str, Any]]:
        """Zbulon gaps në knowledge base"""
        gaps = []
        
        # Simulim: në realitet do lexonte nga ALBI insights
        if self.albi and len(self.albi._insights) > 0:
            for insight in self.albi._insights[-5:]:
                if insight.summary.get("confidence", 1.0) < 0.7:
                    gaps.append({
                        "domain": "neural_patterns",
                        "missing_concept": "low_confidence_pattern",
                        "suggested_source": "pubmed",
                        "confidence": insight.summary.get("confidence")
                    })
        
        return gaps
    
    # ==================== CYCLE EXECUTION ====================
    
    async def start_cycle(self, cycle_id: str) -> CycleExecution:
        """▶️ Nis ekzekutimin e një cycle"""
        if cycle_id not in self.cycles:
            raise ValueError(f"Cycle {cycle_id} not found")
        
        cycle = self.cycles[cycle_id]
        execution = CycleExecution(cycle_id=cycle_id)
        self.executions[cycle_id].append(execution)
        
        cycle.status = CycleStatus.ACTIVE
        self.metrics["active_cycles"] += 1
        
        # Nis ekzekutimin sipas tipit
        if cycle.cycle_type == CycleType.INTERVAL:
            task = asyncio.create_task(self._run_interval_cycle(cycle, execution))
            self.active_tasks[cycle_id] = task
        
        elif cycle.cycle_type == CycleType.EVENT:
            task = asyncio.create_task(self._run_event_cycle(cycle, execution))
            self.active_tasks[cycle_id] = task
        
        elif cycle.cycle_type == CycleType.STREAM:
            task = asyncio.create_task(self._run_stream_cycle(cycle, execution))
            self.active_tasks[cycle_id] = task
        
        elif cycle.cycle_type == CycleType.GAP_TRIGGERED:
            await self._run_gap_cycle(cycle, execution)
        
        elif cycle.cycle_type == CycleType.BATCH:
            await self._run_batch_cycle(cycle, execution)
        
        print(f"▶️ Started: {cycle_id} ({cycle.domain}/{cycle.task})")
        return execution
    
    async def _run_interval_cycle(self, cycle: CycleDefinition, execution: CycleExecution):
        """Ekzekuton cycle me interval"""
        interval = cycle.interval or 60.0
        
        while cycle.status == CycleStatus.ACTIVE:
            try:
                # Ekzekuto detyrën
                result = await self._execute_task(cycle, execution)
                
                # Check alignment
                if not await self._check_alignment(cycle, result):
                    cycle.status = CycleStatus.BLOCKED
                    execution.status = CycleStatus.BLOCKED
                    print(f"🚫 BLOCKED: {cycle.cycle_id} (alignment violation)")
                    break
                
                # Update metrics
                execution.data_processed += result.get("items_processed", 0)
                execution.insights_generated += result.get("insights", 0)
                
                await asyncio.sleep(interval)
            
            except Exception as e:
                execution.error = str(e)
                execution.status = CycleStatus.FAILED
                cycle.status = CycleStatus.FAILED
                print(f"❌ FAILED: {cycle.cycle_id} - {e}")
                break
        
        execution.completed_at = datetime.now(timezone.utc)
        self.metrics["active_cycles"] -= 1
        self.metrics["completed_cycles"] += 1
    
    async def _run_event_cycle(self, cycle: CycleDefinition, execution: CycleExecution):
        """Ekzekuton cycle me event trigger"""
        while cycle.status == CycleStatus.ACTIVE:
            # Pret për event
            triggered = await self._wait_for_event(cycle.event_trigger)
            
            if triggered:
                result = await self._execute_task(cycle, execution)
                
                # Nëse kërkon human review
                if "human-review" in cycle.metadata:
                    cycle.status = CycleStatus.HUMAN_REVIEW
                    execution.status = CycleStatus.HUMAN_REVIEW
                    print(f"👤 HUMAN REVIEW REQUIRED: {cycle.cycle_id}")
                    break
                
                execution.data_processed += result.get("items_processed", 0)
            
            await asyncio.sleep(1.0)
    
    async def _run_stream_cycle(self, cycle: CycleDefinition, execution: CycleExecution):
        """Ekzekuton continuous streaming cycle"""
        while cycle.status == CycleStatus.ACTIVE:
            result = await self._execute_task(cycle, execution)
            execution.data_processed += result.get("items_processed", 0)
            await asyncio.sleep(0.1)  # High frequency
    
    async def _run_gap_cycle(self, cycle: CycleDefinition, execution: CycleExecution):
        """Ekzekuton gap-filling cycle (Born-Concepts)"""
        print(f"🧠 Gap cycle: {cycle.metadata.get('gap_info', {}).get('missing_concept')}")
        
        result = await self._execute_task(cycle, execution)
        
        if result.get("gap_filled"):
            execution.gaps_detected = 1
            self.metrics["gaps_filled"] += 1
            print(f"✓ Gap filled: {cycle.metadata.get('concept')}")
        
        execution.completed_at = datetime.now(timezone.utc)
        execution.status = CycleStatus.COMPLETED
        cycle.status = CycleStatus.COMPLETED
    
    async def _run_batch_cycle(self, cycle: CycleDefinition, execution: CycleExecution):
        """Ekzekuton one-time batch cycle"""
        result = await self._execute_task(cycle, execution)
        execution.data_processed = result.get("items_processed", 0)
        execution.completed_at = datetime.now(timezone.utc)
        execution.status = CycleStatus.COMPLETED
        cycle.status = CycleStatus.COMPLETED
    
    async def _execute_task(self, cycle: CycleDefinition, execution: CycleExecution) -> Dict[str, Any]:
        """Ekzekuton detyrën aktuale të cycle"""
        result = {
            "items_processed": 0,
            "insights": 0,
            "gap_filled": False,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Zgjedh agent dhe ekzekuto
        if cycle.agent == "ALBA" and self.alba:
            # ALBA collection
            if cycle.task == "frequency_monitor":
                # Simulon EEG monitoring
                result["items_processed"] = 1
                result["frequency_data"] = {"alpha": 10.5, "beta": 15.2}
            
            elif cycle.task == "literature_ingest":
                # Simulon PubMed ingestion
                result["items_processed"] = 10
                result["source"] = cycle.source
        
        elif cycle.agent == "ALBI" and self.albi:
            # ALBI analysis
            if cycle.task == "gap_fill":
                # Born-Concepts logic
                result["gap_filled"] = True
                result["new_concept"] = cycle.metadata.get("concept")
            
            elif cycle.task == "anomaly_scan":
                result["insights"] = 3
                result["anomalies_found"] = ["spike_t1", "drift_t2"]
        
        elif cycle.agent == "JONA" and self.jona:
            # JONA oversight
            if cycle.task == "stress_alert":
                result["alert_sent"] = True
                result["severity"] = "high"
        
        return result
    
    async def _check_alignment(self, cycle: CycleDefinition, result: Dict[str, Any]) -> bool:
        """Kontrollon alignment policy"""
        if cycle.alignment == AlignmentPolicy.ETHICAL_GUARD:
            # JONA vendos
            if self.jona:
                health = self.jona.get_health_report()
                if health["🌸 overall_health"] in ["poor", "critical"]:
                    return False
        
        elif cycle.alignment == AlignmentPolicy.STRICT:
            # Çdo gabim ndal
            if result.get("error") or result.get("confidence", 1.0) < 0.9:
                return False
        
        return True
    
    async def _wait_for_event(self, trigger: Optional[str]) -> bool:
        """Pret për një event (simulim)"""
        # Në realitet do monitoronte event streams
        await asyncio.sleep(5.0)
        return True
    
    # ==================== CYCLE MANAGEMENT ====================
    
    def stop_cycle(self, cycle_id: str) -> bool:
        """⏹️ Ndalon një cycle"""
        if cycle_id not in self.cycles:
            return False
        
        cycle = self.cycles[cycle_id]
        cycle.status = CycleStatus.PAUSED
        
        if cycle_id in self.active_tasks:
            self.active_tasks[cycle_id].cancel()
            del self.active_tasks[cycle_id]
        
        self.metrics["active_cycles"] -= 1
        print(f"⏹️ Stopped: {cycle_id}")
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """📊 Status i përgjithshëm (stil njerëzor)"""
        alba_status = "IDLE"
        albi_status = "IDLE"
        jona_status = "IDLE"
        alignment_status = "SAFE MODE"
        
        if self.alba:
            alba_status = "ACTIVE" if len(self.alba._history) > 0 else "IDLE"
        
        if self.albi:
            albi_status = "ACTIVE" if len(self.albi._insights) > 0 else "IDLE"
        
        if self.jona:
            health = self.jona.get_health_report()
            if health["🚨 active_alerts"] > 0:
                jona_status = "Review required"
                alignment_status = "ATTENTION NEEDED"
        
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "ALBA": alba_status,
            "ALBI": albi_status,
            "JONA": jona_status,
            "Alignment": alignment_status,
            "metrics": self.metrics,
            "active_cycles": len([c for c in self.cycles.values() if c.status == CycleStatus.ACTIVE]),
            "pending_gaps": len(self.concept_gaps)
        }
    
    def list_cycles(self, status: Optional[str] = None) -> List[CycleDefinition]:
        """📋 Liston cycles"""
        if status:
            return [c for c in self.cycles.values() if c.status == CycleStatus(status)]
        return list(self.cycles.values())
    
    def get_executions(self, cycle_id: str) -> List[CycleExecution]:
        """📜 History e ekzekutimeve"""
        return self.executions.get(cycle_id, [])


# ==================== CLI INTERFACE ====================

async def cli_main():
    """CLI për Cycle Engine"""
    import sys
    
    if len(sys.argv) < 2:
        print("""
🔁 CYCLE ENGINE - Usage:

  python cycle_engine.py create --domain neuro --source alba.eeg --task monitor --interval 1
  python cycle_engine.py create --domain scientific --source pubmed --task ingest --interval 86400
  python cycle_engine.py create --event "beta>25Hz" --task stress_alert --agent JONA
  python cycle_engine.py auto-create --trigger low_confidence --max 10
  python cycle_engine.py start <cycle_id>
  python cycle_engine.py stop <cycle_id>
  python cycle_engine.py status
  python cycle_engine.py list [--status active]
        """)
        return
    
    engine = CycleEngine()
    command = sys.argv[1]
    
    if command == "create":
        # Parse arguments
        args = {}
        for i in range(2, len(sys.argv), 2):
            if i+1 < len(sys.argv):
                key = sys.argv[i].lstrip("--")
                value = sys.argv[i+1]
                args[key] = value
        
        cycle = engine.create_cycle(**args)
        print(json.dumps({
            "cycle_id": cycle.cycle_id,
            "domain": cycle.domain,
            "task": cycle.task,
            "status": cycle.status.value
        }, indent=2))
    
    elif command == "auto-create":
        trigger = "low_confidence"
        max_cycles = 10
        for i in range(2, len(sys.argv)):
            if sys.argv[i] == "--trigger" and i+1 < len(sys.argv):
                trigger = sys.argv[i+1]
            elif sys.argv[i] == "--max" and i+1 < len(sys.argv):
                max_cycles = int(sys.argv[i+1])
        
        cycles = engine.auto_create_cycles(trigger=trigger, max_cycles=max_cycles)
        print(json.dumps([{"cycle_id": c.cycle_id, "domain": c.domain} for c in cycles], indent=2))
    
    elif command == "start" and len(sys.argv) > 2:
        cycle_id = sys.argv[2]
        execution = await engine.start_cycle(cycle_id)
        print(json.dumps({"execution_id": execution.execution_id, "status": execution.status.value}, indent=2))
    
    elif command == "stop" and len(sys.argv) > 2:
        cycle_id = sys.argv[2]
        result = engine.stop_cycle(cycle_id)
        print(json.dumps({"stopped": result}, indent=2))
    
    elif command == "status":
        status = engine.get_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))
    
    elif command == "list":
        status_filter = None
        if "--status" in sys.argv:
            idx = sys.argv.index("--status")
            if idx+1 < len(sys.argv):
                status_filter = sys.argv[idx+1]
        
        cycles = engine.list_cycles(status=status_filter)
        print(json.dumps([{
            "cycle_id": c.cycle_id,
            "domain": c.domain,
            "task": c.task,
            "status": c.status.value
        } for c in cycles], indent=2))


if __name__ == "__main__":
    asyncio.run(cli_main())

