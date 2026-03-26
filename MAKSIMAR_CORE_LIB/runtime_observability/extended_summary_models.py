from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ExtendedSummaryLine:
    """One extended observability summary line."""

    metric_name: str
    metric_value: int
    metric_unit: str


@dataclass(frozen=True, slots=True)
class ExtendedObservabilitySummary:
    """Unified extended observability summary contract."""

    overall_status: str
    total_lines: int
    lines: tuple[ExtendedSummaryLine, ...]
