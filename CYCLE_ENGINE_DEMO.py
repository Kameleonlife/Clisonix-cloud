#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔁 CYCLE ENGINE - DEMONSTRIM I PLOTË
====================================
Shembuj praktikë të të gjitha llojeve të cycles
"""

import asyncio
import json
from cycle_engine import CycleEngine, CycleType, AlignmentPolicy

async def demo():
    print("=" * 70)
    print("🔁 CYCLE ENGINE - DEMONSTRIM")
    print("=" * 70)
    
    engine = CycleEngine()
    
    # ==================== 1️⃣ NEURO MONITORING ====================
    print("\n1️⃣ NEURO / EEG MONITORING")
    print("-" * 70)
    
    neuro_cycle = engine.create_cycle(
        domain="neuro",
        source="alba.eeg.stream",
        agent="ALBA",
        task="frequency_monitor",
        cycle_type="interval",
        interval=1.0,
        alignment="strict"
    )
    print(f"✓ Created: {neuro_cycle.cycle_id}")
    print(f"  Domain: {neuro_cycle.domain}")
    print(f"  Task: {neuro_cycle.task}")
    print(f"  Agent: {neuro_cycle.agent}")
    print(f"  Interval: {neuro_cycle.interval}s")
    
    # ==================== 2️⃣ SCIENTIFIC LITERATURE ====================
    print("\n2️⃣ OPEN DATA / PUBMED INGESTION")
    print("-" * 70)
    
    pubmed_cycle = engine.create_cycle(
        domain="scientific",
        source="pubmed",
        task="literature_ingest",
        cycle_type="interval",
        interval=86400,  # 24h
        target=["weaviate", "neo4j"],
        alignment="moderate",
        on_gap="born-concept"
    )
    print(f"✓ Created: {pubmed_cycle.cycle_id}")
    print(f"  Domain: {pubmed_cycle.domain}")
    print(f"  Refresh: every 24h")
    print(f"  Target: {pubmed_cycle.target_storage}")
    print(f"  On Gap: Born-Concept triggered")
    
    # ==================== 3️⃣ EVENT-BASED (STRESS ALERT) ====================
    print("\n3️⃣ EVENT-BASED / STRESS DETECTION")
    print("-" * 70)
    
    stress_cycle = engine.create_cycle(
        domain="neuro",
        event_trigger="beta>25Hz",
        task="stress_alert",
        agent="JONA",
        cycle_type="event",
        alignment="ethical_guard",
        require_human_review=True
    )
    print(f"✓ Created: {stress_cycle.cycle_id}")
    print(f"  Trigger: {stress_cycle.event_trigger}")
    print(f"  Agent: {stress_cycle.agent} (JONA will review)")
    print(f"  Human Review: Required")
    
    # ==================== 4️⃣ INDUSTRIAL TELEMETRY ====================
    print("\n4️⃣ INDUSTRIAL / FIWARE TELEMETRY")
    print("-" * 70)
    
    industrial_cycle = engine.create_cycle(
        domain="industrial",
        source="fiware.context",
        agent="ALBI",
        task="anomaly_scan",
        cycle_type="interval",
        interval=5.0,
        target=["timescale"],
        alignment="moderate"
    )
    print(f"✓ Created: {industrial_cycle.cycle_id}")
    print(f"  Domain: {industrial_cycle.domain}")
    print(f"  Task: {industrial_cycle.task}")
    print(f"  Storage: TimescaleDB")
    
    # ==================== 5️⃣ AUTO-CREATE (GAPS) ====================
    print("\n5️⃣ AUTO-CREATE / BORN-CONCEPTS")
    print("-" * 70)
    
    auto_cycles = engine.auto_create_cycles(
        trigger="low_confidence",
        max_cycles=3,
        domain="neural_patterns"
    )
    print(f"✓ Auto-created: {len(auto_cycles)} cycles")
    for cycle in auto_cycles:
        print(f"  - {cycle.cycle_id}: {cycle.domain}/{cycle.task}")
    
    # ==================== 6️⃣ LIST ALL CYCLES ====================
    print("\n6️⃣ ALL CYCLES")
    print("-" * 70)
    
    all_cycles = engine.list_cycles()
    print(f"Total: {len(all_cycles)} cycles\n")
    
    for cycle in all_cycles:
        status_emoji = {
            "pending": "⏳",
            "active": "▶️",
            "paused": "⏸️",
            "completed": "✅",
            "failed": "❌",
            "blocked": "🚫"
        }.get(cycle.status.value, "❓")
        
        print(f"{status_emoji} {cycle.cycle_id}")
        print(f"   Domain: {cycle.domain} | Task: {cycle.task}")
        print(f"   Agent: {cycle.agent} | Type: {cycle.cycle_type.value}")
        print(f"   Status: {cycle.status.value}")
        print()
    
    # ==================== 7️⃣ SYSTEM STATUS ====================
    print("\n7️⃣ SYSTEM STATUS")
    print("-" * 70)
    
    status = engine.get_status()
    print(f"ALBA: {status['ALBA']}")
    print(f"ALBI: {status['ALBI']}")
    print(f"JONA: {status['JONA']}")
    print(f"Alignment: {status['Alignment']}")
    print(f"\nMetrics:")
    for key, value in status['metrics'].items():
        print(f"  {key}: {value}")
    
    # ==================== 8️⃣ START A CYCLE (DEMO) ====================
    print("\n8️⃣ STARTING NEURO CYCLE (5s demo)")
    print("-" * 70)
    
    execution = await engine.start_cycle(neuro_cycle.cycle_id)
    print(f"✓ Started: {execution.execution_id}")
    print(f"  Status: {execution.status.value}")
    
    # Run for 5 seconds
    await asyncio.sleep(5)
    
    # Stop
    engine.stop_cycle(neuro_cycle.cycle_id)
    print(f"⏹️ Stopped: {neuro_cycle.cycle_id}")
    
    # Get execution history
    executions = engine.get_executions(neuro_cycle.cycle_id)
    if executions:
        last_exec = executions[-1]
        print(f"\nExecution Summary:")
        print(f"  Data processed: {last_exec.data_processed}")
        print(f"  Insights: {last_exec.insights_generated}")
        print(f"  Alignment score: {last_exec.alignment_score}")
    
    # ==================== 9️⃣ FINAL STATUS ====================
    print("\n9️⃣ FINAL STATUS")
    print("-" * 70)
    
    final_status = engine.get_status()
    print(json.dumps(final_status, indent=2, ensure_ascii=False))
    
    print("\n" + "=" * 70)
    print("✅ DEMO COMPLETED")
    print("=" * 70)
    print("\nKY ËSHTË VIZION UNIK! 🚀")
    print("Cycle Engine integron:")
    print("  ✓ ALBA, ALBI, JONA")
    print("  ✓ Open Data (PubMed, FIWARE)")
    print("  ✓ Born-Concepts (auto gap-filling)")
    print("  ✓ Ethical alignment (JONA oversight)")
    print("  ✓ Multi-domain (neuro, scientific, industrial)")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(demo())

