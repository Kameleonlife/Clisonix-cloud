"""Economy layer for translating AGIEM cycle output into NeuroCredit metrics."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Dict, List
from uuid import uuid4


@dataclass
class EconomyTransaction:
    identifier: str
    recorded_at: str
    credits_nc: float
    components: Dict[str, float]
    payload: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class EconomyLayer:
    """In-memory economic model for a single center."""

    def __init__(self, *, center_name: str, specialization: str) -> None:
        self.center_name = center_name
        self.specialization = specialization
        self._lock = Lock()
        self._transactions: List[EconomyTransaction] = []
        self._totals_nc = 0.0
        self._sector_totals: Dict[str, float] = {
            "data_intelligence": 0.0,
            "alignment_security": 0.0,
            "api_generation": 0.0,
            "operations": 0.0,
        }

    # ------------------------------------------------------------------
    # cycle accounting
    # ------------------------------------------------------------------
    def compute_cycle_value(
        self,
        *,
        alba_frames: int,
        albi_insights: int,
        jona_validations: int,
        asi_apis: int,
    ) -> Dict[str, Any]:
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        credits = self._calculate_credits(alba_frames, albi_insights, jona_validations, asi_apis)
        components = self._distribute_components(alba_frames, albi_insights, jona_validations, asi_apis, credits)
        transaction = EconomyTransaction(
            identifier=str(uuid4()),
            recorded_at=timestamp,
            credits_nc=round(credits, 2),
            components=components,
            payload={
                "alba_frames": int(alba_frames),
                "albi_insights": int(albi_insights),
                "jona_validations": int(jona_validations),
                "asi_apis": int(asi_apis),
            },
        )
        with self._lock:
            self._totals_nc += transaction.credits_nc
            for key, value in components.items():
                self._sector_totals[key] = round(self._sector_totals.get(key, 0.0) + value, 2)
            self._transactions.append(transaction)
        return transaction.to_dict()

    def generate_report(self) -> Dict[str, Any]:
        with self._lock:
            total_transactions = len(self._transactions)
            latest = self._transactions[-1].to_dict() if self._transactions else None
            return {
                "center": self.center_name,
                "specialization": self.specialization,
                "transactions_count": total_transactions,
                "estimated_gdp_NC": round(self._totals_nc, 2),
                "sector_distribution": {k: round(v, 2) for k, v in self._sector_totals.items()},
                "latest_transaction": latest,
            }

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    def _calculate_credits(
        self,
        alba_frames: int,
        albi_insights: int,
        jona_validations: int,
        asi_apis: int,
    ) -> float:
        base_unit = 42.0
        weighted_sum = (
            (alba_frames * 1.2)
            + (albi_insights * 2.4)
            + (jona_validations * 1.8)
            + (asi_apis * 2.7)
        )
        credits = base_unit * weighted_sum
        return max(0.0, credits)

    def _distribute_components(
        self,
        alba_frames: int,
        albi_insights: int,
        jona_validations: int,
        asi_apis: int,
        credits_total: float,
    ) -> Dict[str, float]:
        data_intelligence = (alba_frames * 18.0) + (albi_insights * 32.0)
        alignment_security = jona_validations * 48.0
        api_generation = asi_apis * 64.0
        allocated = data_intelligence + alignment_security + api_generation
        operations = max(credits_total - allocated, 0.0)
        return {
            "data_intelligence": round(data_intelligence, 2),
            "alignment_security": round(alignment_security, 2),
            "api_generation": round(api_generation, 2),
            "operations": round(operations, 2),
        }


__all__ = ["EconomyLayer", "EconomyTransaction"]

