"""Minimal ASI system stub.

This module provides a lightweight, safe stub implementation of an "ASI system"
for local development and tests. It intentionally avoids external dependencies
and network calls. The class here can be imported by other modules that expect
an ASI-like interface while you build the real implementation.

Public API:
- ASISystem: simple class with start(), stop(), and health_check().
- run_cli(): a tiny CLI entrypoint for manual smoke testing.

The code is purposefully minimal to keep tests fast and deterministic.
"""
from __future__ import annotations

import threading
import time
from typing import Optional


class ASISystem:
	"""A tiny stub representing an ASI system.

	Usage:
		system = ASISystem(name="dev-asi")
		system.start()
		ok = system.health_check()
		system.stop()

	This is NOT a production implementation. It's intended to be used where the
	repository expects an object with start/stop/health_check semantics.
	"""

	def __init__(self, name: str = "asi-local") -> None:
		self.name = name
		self._running = False
		self._lock = threading.RLock()
		self._uptime_start: Optional[float] = None

	def start(self) -> None:
		"""Start the stub system. Sets an internal running flag and timestamp.

		This method is idempotent.
		"""
		with self._lock:
			if self._running:
				return
			self._running = True
			self._uptime_start = time.time()

	def stop(self) -> None:
		"""Stop the stub system. Idempotent."""
		with self._lock:
			if not self._running:
				return
			self._running = False
			self._uptime_start = None

	def health_check(self) -> dict:
		"""Return a small health dict describing the system state.

		Returns a dictionary with keys:
		- status: 'running' or 'stopped'
		- name: configured name
		- uptime_seconds: float (0 if stopped)
		"""
		with self._lock:
			status = "running" if self._running else "stopped"
			uptime = 0.0
			if self._running and self._uptime_start is not None:
				uptime = time.time() - self._uptime_start
			return {"status": status, "name": self.name, "uptime_seconds": uptime}


def run_cli() -> int:
	"""Simple CLI runner used for manual smoke tests.

	Starts the system for a short period, prints health, and exits.
	Returns 0 on success.
	"""
	sys = ASISystem(name="asi-cli-test")
	sys.start()
	health = sys.health_check()
	print("ASI System started (stub) ->", health)
	# keep running a tiny bit to produce non-zero uptime
	time.sleep(0.05)
	health2 = sys.health_check()
	print("ASI System health after short sleep ->", health2)
	sys.stop()
	print("ASI System stopped")
	return 0


if __name__ == "__main__":
	raise SystemExit(run_cli())


