from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExecutionSummaryLine:
    """Canonical execution summary line."""

    metric_name: str
    value: int
    status: str


@dataclass(frozen=True, slots=True)
class ExecutionSummary:
    """Unified execution summary."""

    overall_status: str
    total_lines: int
    lines: tuple[ExecutionSummaryLine, ...]
