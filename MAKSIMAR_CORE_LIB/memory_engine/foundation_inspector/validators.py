from __future__ import annotations

from pathlib import Path
from typing import Any


def validate_runtime_state_path(path: Path) -> None:
    """Validate runtime state artifact path."""

    if not path.is_absolute():
        raise ValueError("runtime state path must be absolute")

    if path.suffix != ".json":
        raise ValueError("runtime state path must point to a .json file")


def validate_memory_heartbeat_payload(payload: dict[str, Any]) -> None:
    """Validate raw memory heartbeat payload before model building."""

    required_keys = {
        "timestamp_wall",
        "timestamp_monotonic",
        "pid",
        "status",
        "source",
    }
    missing_keys = required_keys.difference(payload)
    if missing_keys:
        missing = ", ".join(sorted(missing_keys))
        raise ValueError(f"heartbeat payload missing required keys: {missing}")

    if not isinstance(payload["timestamp_wall"], str) or not payload["timestamp_wall"]:
        raise ValueError("timestamp_wall must be a non-empty string")

    if not isinstance(payload["timestamp_monotonic"], (int, float)):
        raise ValueError("timestamp_monotonic must be numeric")

    if float(payload["timestamp_monotonic"]) < 0:
        raise ValueError("timestamp_monotonic must be >= 0")

    if not isinstance(payload["pid"], int) or payload["pid"] <= 0:
        raise ValueError("pid must be a positive integer")

    if payload["status"] not in {"alive", "stopped"}:
        raise ValueError("status must be one of {'alive', 'stopped'}")

    if not isinstance(payload["source"], str) or not payload["source"]:
        raise ValueError("source must be a non-empty string")
