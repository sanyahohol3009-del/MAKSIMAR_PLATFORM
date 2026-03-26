from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionObservabilityShellContract:
    """Final shell contract for execution observability."""

    shell_id: str
    total_metrics: int
    total_summary_lines: int
    total_alerts: int
    total_incidents: int
    total_traces: int
    overall_status: str
