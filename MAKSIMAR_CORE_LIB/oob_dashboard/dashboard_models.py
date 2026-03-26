from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DashboardStateLine:
    """One read-only dashboard state line."""

    source_name: str
    status: str
    detail_value: int


@dataclass(frozen=True, slots=True)
class DashboardStateSnapshot:
    """Unified read-only dashboard snapshot."""

    overall_status: str
    total_lines: int
    lines: list[DashboardStateLine]
