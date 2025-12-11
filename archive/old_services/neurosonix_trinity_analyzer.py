# -*- coding: utf-8 -*-
"""
Clisonix Trinity Analyzer
Hashes the status of the ALBA, ALBI, and JONA modules and produces a deep insight report.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List


def analyze_trinity_status(data: Dict[str, Any]) -> Dict[str, Any]:
    analysis: Dict[str, Any] = {
        "timestamp": datetime.utcnow().isoformat(),
        "insights": [],
    }

    trinity: Dict[str, Dict[str, Any]] = data.get("trinity", {})
    health_scores: List[float] = []

    for module_name, node in trinity.items():
        health = float(node.get("health", 0.0))
        status = node.get("status", "unknown")
        role = node.get("role", "undefined")

        if health >= 0.90:
            state = "optimal"
            comment = f"{module_name.upper()} is operating at full performance ({health * 100:.1f}%)."
        elif health >= 0.70:
            state = "stable"
            comment = f"{module_name.upper()} is stable but should be monitored for CPU and IO spikes."
        else:
            state = "critical"
            comment = f"{module_name.upper()} is below the safety threshold ({health * 100:.1f}%). Technical intervention required."

        insight = {
            "module": module_name.upper(),
            "role": role,
            "status": status,
            "health_score": health,
            "state": state,
            "comment": comment,
        }

        health_scores.append(health)
        analysis["insights"].append(insight)

    average = sum(health_scores) / len(health_scores) if health_scores else 0.0
    if average >= 0.90:
        summary = "Trinity system is performing optimally."
    elif average >= 0.75:
        summary = "System is functional, but at least one module needs attention."
    else:
        summary = "System in critical condition. Immediate intervention required."

    analysis["system_health_index"] = round(average, 3)
    analysis["summary"] = summary

    return analysis


if __name__ == "__main__":
    demo_payload = {
        "status": "operational",
        "trinity": {
            "alba": {"status": "active", "role": "network_monitor", "health": 0.92},
            "albi": {"status": "active", "role": "neural_processor", "health": 0.88},
            "jona": {"status": "active", "role": "data_coordinator", "health": 0.95},
        },
        "system": {"version": "2.1.0", "uptime": 44.04, "instance": "alpha7"},
    }

    report = analyze_trinity_status(demo_payload)
    from pprint import pprint

    pprint(report)
