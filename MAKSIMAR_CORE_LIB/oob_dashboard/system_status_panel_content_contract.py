from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_status_panel_summary_contract import (
    build_foundation_status_panel_summary_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.foundation_unified_dashboard_view import (
    build_foundation_unified_dashboard_view,
)


UnifiedSystemStatus = Literal[
    "active",
    "degraded",
]


@dataclass(frozen=True, slots=True)
class SystemStatusPanelContentEntry:
    """Canonical content entry for the system-status panel."""

    panel_id: str
    runtime_panel_id: str
    guard_panel_id: str
    core_guard_panel_id: str
    kernel_guard_panel_id: str
    unified_system_status: UnifiedSystemStatus
    total_foundation_entries: int
    visible_in_main_dashboard: bool
    visible_in_oob_dashboard: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class SystemStatusPanelContentContract:
    """Canonical content contract for the system-status panel."""

    total_entries: int
    read_only_entries: int
    main_dashboard_visible_entries: int
    oob_visible_entries: int
    entries: tuple[SystemStatusPanelContentEntry, ...]


def build_system_status_panel_content_contract() -> (
    SystemStatusPanelContentContract
):
    """Build canonical content contract for the system-status panel."""
    foundation_summary_contract = build_foundation_status_panel_summary_contract()
    unified_dashboard_view = build_foundation_unified_dashboard_view()

    summary_ids = [entry.panel_id for entry in foundation_summary_contract.entries]

    entries = (
        SystemStatusPanelContentEntry(
            panel_id="panel_system_status_001",
            runtime_panel_id="panel_foundation_runtime_status_001",
            guard_panel_id="panel_foundation_guard_status_001",
            core_guard_panel_id="panel_foundation_core_guard_status_001",
            kernel_guard_panel_id="panel_foundation_kernel_guard_status_001",
            unified_system_status=(
                "active"
                if unified_dashboard_view.degraded_panels == 0
                else "degraded"
            ),
            total_foundation_entries=len(summary_ids),
            visible_in_main_dashboard=True,
            visible_in_oob_dashboard=True,
            read_only=True,
            description=(
                "Canonical system-status panel content contract built from "
                "foundation summary entries and unified dashboard view."
            ),
        ),
    )

    return SystemStatusPanelContentContract(
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        main_dashboard_visible_entries=sum(
            1 for entry in entries if entry.visible_in_main_dashboard
        ),
        oob_visible_entries=sum(
            1 for entry in entries if entry.visible_in_oob_dashboard
        ),
        entries=entries,
    )
