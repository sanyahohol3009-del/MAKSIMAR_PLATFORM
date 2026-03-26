from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeObservabilityShellContract:
    """Final shell contract for runtime observability extension."""

    shell_id: str
    total_metrics: int
    total_spans: int
    total_log_records: int
    total_config_entries: int
    total_slo_indicators: int
    overall_status: str
