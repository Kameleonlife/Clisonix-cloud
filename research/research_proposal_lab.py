"""Research and proposal support utilities for the ASI reproduction pipeline."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ResearchBrief:
    """High-level brief summarising the current reproduction cycle."""

    title: str
    executive_summary: str
    key_findings: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    data_highlights: Dict[str, Any] = field(default_factory=dict)
    generated_assets: Dict[str, Any] = field(default_factory=dict)
    strategic_alignment: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class ProposalPacket:
    """Full packet with metadata and persisted location."""

    brief: ResearchBrief
    packet_path: Optional[Path]
    attachments: Dict[str, Path] = field(default_factory=dict)


class ResearchProposalLab:
    """Transforms telemetry and generated APIs into proposal-ready artefacts."""

    def __init__(self, *, output_root: Path | str = Path("generated_proposals")) -> None:
        self.output_root = Path(output_root)
        self.output_root.mkdir(parents=True, exist_ok=True)

    def build_brief(self, context: Dict[str, Any]) -> ResearchBrief:
        alignment = context.get("alignment") or {}
        insight = context.get("insight") or {}
        api_summary = context.get("generated_api") or {}
        center = context.get("center")
        specialization = context.get("specialization") or api_summary.get("domain")

        title = f"{specialization.title() if isinstance(specialization, str) else 'ASI'} Proposal Brief"
        summary_parts: List[str] = []
        if center:
            summary_parts.append(f"Center: {center.get('name', center)}")
        if alignment.get("status"):
            summary_parts.append(f"Alignment status: {alignment['status']}")
        if api_summary.get("domain"):
            summary_parts.append(f"Generated API: {api_summary['domain']}")
        executive_summary = " | ".join(summary_parts) if summary_parts else "Automated proposal brief"

        key_findings: List[str] = []
        if insight.get("summary"):
            key_findings.append("Latest insight averages captured for reference")
        if alignment.get("focus_channels"):
            key_findings.append("Alignment review required for focus channels")
        if not key_findings:
            key_findings.append("No anomalies detected; operating within nominal thresholds")

        recommended_actions: List[str] = []
        if alignment.get("focus_channels"):
            recommended_actions.append(
                "Coordinate targeted remediation on focus channels before next reproduction cycle"
            )
        if api_summary:
            recommended_actions.append("Review generated API spec and schedule domain validation")

        data_highlights = {
            "alignment": alignment,
            "insight": insight,
        }
        generated_assets = {
            "api": api_summary,
        }
        if "alba_summary" in context:
            data_highlights["alba"] = context["alba_summary"]
        if "albi_recommendations" in context:
            data_highlights["albi"] = context["albi_recommendations"]

        strategic_alignment = {
            "priority": api_summary.get("priority") if api_summary else context.get("priority"),
            "tags": api_summary.get("tags") if api_summary else context.get("tags"),
        }
        if center:
            strategic_alignment["center"] = center

        return ResearchBrief(
            title=title,
            executive_summary=executive_summary,
            key_findings=key_findings,
            recommended_actions=recommended_actions,
            data_highlights=data_highlights,
            generated_assets=generated_assets,
            strategic_alignment=strategic_alignment,
        )

    def persist_packet(
        self,
        brief: ResearchBrief,
        *,
        filename_prefix: Optional[str] = None,
        attachments: Optional[Dict[str, Path]] = None,
    ) -> ProposalPacket:
        prefix = filename_prefix or brief.title.lower().replace(" ", "-")
        packet_path = self.output_root / f"{prefix}_packet.json"
        packet_payload = {
            "brief": brief.__dict__,
            "attachments": {k: str(v) for k, v in (attachments or {}).items()},
        }
        packet_path.write_text(json.dumps(packet_payload, indent=2), encoding="utf-8")
        return ProposalPacket(brief=brief, packet_path=packet_path, attachments=attachments or {})
