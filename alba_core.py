"""Alba Core – real data collection layer for the Trinity stack.

This module avoids external dependencies so it can operate in constrained
environments while still providing meaningful telemetry about EEG/industrial
signals flowing through the system.

Key concepts
------------
* ``SignalFrame`` records a single capture with channel amplitudes.
* ``AlbaCore`` manages a rolling history, calculates light-weight metrics and
  persists them when needed.

The implementation is intentionally deterministic: all numeric operations use
the standard library so unit tests stay fast and predictable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Any, Optional, Iterable

import json
import statistics
import time


@dataclass(frozen=True)
class SignalFrame:
	"""Single signal capture stored by ALBA."""

	timestamp: float
	channels: Dict[str, float]
	metadata: Dict[str, Any] = field(default_factory=dict)

	def band_power(self) -> float:
		"""Return simple band power estimation."""

		return sum(self.channels.values()) / max(len(self.channels), 1)


class AlbaCore:
	"""Rolling signal collector with basic statistics."""

	def __init__(self, *, max_history: int = 2048, auto_start: bool = True) -> None:
		self.max_history = max(1, max_history)
		self.auto_start = auto_start
		self._history: List[SignalFrame] = []
		self._status: str = "idle"
		self._started_at: Optional[float] = None

	# --------------------------------------------------------------
	# lifecycle helpers
	# --------------------------------------------------------------
	def start(self) -> None:
		if self._status == "running":
			return
		self._status = "running"
		self._started_at = time.time()

	def stop(self) -> None:
		if self._status == "idle":
			return
		self._status = "idle"
		self._started_at = None

	# --------------------------------------------------------------
	# ingestion
	# --------------------------------------------------------------
	def ingest(
		self,
		channels: Dict[str, float],
		*,
		metadata: Optional[Dict[str, Any]] = None,
		timestamp: Optional[float] = None,
	) -> SignalFrame:
		if self._status != "running" and self.auto_start:
			self.start()

		clean_channels = {k: float(v) for k, v in channels.items()}
		frame = SignalFrame(timestamp=timestamp or time.time(), channels=clean_channels, metadata=metadata or {})
		self._history.append(frame)
		if len(self._history) > self.max_history:
			self._history = self._history[-self.max_history :]
		return frame

	def ingest_batch(self, frames: Iterable[Dict[str, Any]]) -> int:
		count = 0
		for entry in frames:
			channels = entry.get("channels") or {}
			metadata = entry.get("metadata") or {}
			ts = entry.get("timestamp")
			self.ingest(channels, metadata=metadata, timestamp=ts)
			count += 1
		return count

	# --------------------------------------------------------------
	# metrics and reporting
	# --------------------------------------------------------------
	def history(self) -> List[SignalFrame]:
		return list(self._history)

	def last_frame(self) -> Optional[SignalFrame]:
		return self._history[-1] if self._history else None

	def average_channel_levels(self) -> Dict[str, float]:
		if not self._history:
			return {}
		sums: Dict[str, List[float]] = {}
		for frame in self._history:
			for channel, value in frame.channels.items():
				sums.setdefault(channel, []).append(value)
		return {channel: statistics.fmean(values) for channel, values in sums.items()}

	def signal_variance(self) -> float:
		if len(self._history) < 2:
			return 0.0
		powers = [frame.band_power() for frame in self._history]
		return statistics.pvariance(powers) if len(powers) > 1 else 0.0

	def health(self) -> Dict[str, Any]:
		uptime = 0.0
		if self._status == "running" and self._started_at:
			uptime = time.time() - self._started_at
		last = self.last_frame()
		return {
			"module": "ALBA",
			"status": self._status,
			"uptime_seconds": uptime,
			"total_frames": len(self._history),
			"last_timestamp": last.timestamp if last else None,
			"avg_channels": self.average_channel_levels(),
			"signal_variance": self.signal_variance(),
		}

	# --------------------------------------------------------------
	# persistence
	# --------------------------------------------------------------
	def export_history(self, target: Path | str) -> Path:
		data = [
			{
				"timestamp": frame.timestamp,
				"channels": frame.channels,
				"metadata": frame.metadata,
			}
			for frame in self._history
		]
		path = Path(target)
		path.write_text(json.dumps(data, indent=2), encoding="utf-8")
		return path

	def load_history(self, source: Path | str) -> int:
		path = Path(source)
		if not path.exists():
			return 0
		payload = json.loads(path.read_text(encoding="utf-8-sig"))
		self._history.clear()
		for entry in payload:
			self.ingest(
				entry.get("channels", {}),
				metadata=entry.get("metadata"),
				timestamp=entry.get("timestamp"),
			)
		return len(self._history)


__all__ = ["SignalFrame", "AlbaCore"]


