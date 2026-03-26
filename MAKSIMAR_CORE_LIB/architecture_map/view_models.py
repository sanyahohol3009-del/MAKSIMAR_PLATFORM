from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DashboardViewEntry:
    """Canonical read-only dashboard architecture view entry."""

    view_id: str
    source_contract: str
    panel_name: str
    read_only: bool


@dataclass(frozen=True, slots=True)
class DashboardViewRegistryContract:
    """Unified dashboard view registry contract."""

    total_views: int
    views: tuple[DashboardViewEntry, ...]
