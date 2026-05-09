from __future__ import annotations

import re
from dataclasses import dataclass


_BINDING_ID_PATTERN = re.compile(r"^retrieval_observability_binding_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class RetrievalObservabilityBinding:
    binding_id: str
    metrics_total_entries: int
    metrics_active_entries: int
    router_binding_entries: int
    route_request_ids: tuple[str, ...]
    trace_binding_ready: bool
    observability_ready: bool

    def __post_init__(self) -> None:
        binding_id = _ensure_non_empty_str(self.binding_id, "binding_id")
        metrics_total_entries = _ensure_non_negative_int(
            self.metrics_total_entries,
            "metrics_total_entries",
        )
        metrics_active_entries = _ensure_non_negative_int(
            self.metrics_active_entries,
            "metrics_active_entries",
        )
        router_binding_entries = _ensure_non_negative_int(
            self.router_binding_entries,
            "router_binding_entries",
        )

        if not _BINDING_ID_PATTERN.fullmatch(binding_id):
            raise ValueError(f"Invalid binding_id: {binding_id}")
        if metrics_total_entries <= 0:
            raise ValueError("metrics_total_entries must be >= 1")
        if metrics_active_entries > metrics_total_entries:
            raise ValueError("metrics_active_entries must not exceed metrics_total_entries")
        if router_binding_entries <= 0:
            raise ValueError("router_binding_entries must be >= 1")
        if not isinstance(self.route_request_ids, tuple):
            raise ValueError("route_request_ids must be a tuple")
        if not self.route_request_ids:
            raise ValueError("route_request_ids must be non-empty")
        if len(set(self.route_request_ids)) != len(self.route_request_ids):
            raise ValueError("route_request_ids must be unique")

        _ensure_bool(self.trace_binding_ready, "trace_binding_ready")
        _ensure_bool(self.observability_ready, "observability_ready")

        if not self.trace_binding_ready:
            raise ValueError("trace_binding_ready must be True")
        if not self.observability_ready:
            raise ValueError("observability_ready must be True")

        object.__setattr__(self, "binding_id", binding_id)
        object.__setattr__(self, "metrics_total_entries", metrics_total_entries)
        object.__setattr__(self, "metrics_active_entries", metrics_active_entries)
        object.__setattr__(self, "router_binding_entries", router_binding_entries)
