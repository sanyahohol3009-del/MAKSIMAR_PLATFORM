from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeMetric:
    """One runtime metric item."""

    metric_name: str
    metric_value: int
    status: str


@dataclass(frozen=True, slots=True)
class RuntimeSnapshot:
    """Unified runtime observability snapshot."""

    runtime_documents: int
    event_records: int
    health_total_domains: int
    health_loaded_domains: int
    health_failed_domains: int
    self_check_total_items: int
