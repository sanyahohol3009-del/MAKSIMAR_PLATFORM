from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeepExecutionObservabilityShellContract:
    """Final shell contract for deep execution observability layer."""

    shell_id: str
    total_queue_metrics: int
    total_lease_metrics: int
    total_pressure_metrics: int
    total_worker_saturation_metrics: int
