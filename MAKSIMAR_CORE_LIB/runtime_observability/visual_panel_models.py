from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


VisualSeverity = Literal[
    "ok",
    "warning",
    "critical",
]


@dataclass(frozen=True, slots=True)
class VisualPanelMetric:
    """One visual-ready observability metric."""

    metric_name: str
    metric_value: int
    metric_unit: str
    severity: VisualSeverity


@dataclass(frozen=True, slots=True)
class RuntimeObservabilityVisualPanel:
    """Visual-ready observability panel contract."""

    panel_id: str
    overall_status: str
    total_metrics: int
    metrics: tuple[VisualPanelMetric, ...]
