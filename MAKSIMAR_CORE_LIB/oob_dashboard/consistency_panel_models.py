from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DashboardConsistencyPanel:
    """Read-only dashboard panel backed by unified consistency report."""

    panel_id: str
    overall_consistent: bool
    total_checks: int
    total_lines: int
    status: str
