# -*- coding: utf-8 -*-
"""
Telemetry / tracing decorator for Clisonix services.
Captures function entry metadata, timing, and approximate payload size without logging contents.
"""

from __future__ import annotations

import functools
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

LOG_PATH = Path(r"C:\Clisonix-cloud\logs\telemetry.jsonl")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


def trace(func: Callable) -> Callable:
    """Decorator that instruments a function call and writes metadata to telemetry.jsonl."""

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        start = time.perf_counter()
        result: Any = None
        error: str | None = None
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as exc:
            error = str(exc)
            raise
        finally:
            end = time.perf_counter()
            duration_ms = (end - start) * 1000.0
            entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "function": func.__name__,
                "args_count": len(args),
                "kwargs_count": len(kwargs),
                "input_bytes": _approx_size(args, kwargs),
                "output_bytes": _approx_size(result),
                "duration_ms": round(duration_ms, 3),
                "error": error,
            }
            with open(LOG_PATH, "a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry) + "\n")

    return wrapper


def _approx_size(*values: Any) -> int:
    """Estimate total size in bytes for the supplied objects."""

    import sys

    total = 0
    for value in values:
        if value is None:
            continue
        try:
            total += sys.getsizeof(value)
        except Exception:
            continue
    return int(total)


__all__ = ["trace"]
