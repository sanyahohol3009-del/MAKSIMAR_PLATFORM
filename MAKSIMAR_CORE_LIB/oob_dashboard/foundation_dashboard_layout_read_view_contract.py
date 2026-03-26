from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


FoundationLayoutZone = Literal[
    "left_menu",
    "center_core",
    "inner_ring",
    "outer_ring",
]

FoundationLayoutViewMode = Literal[
    "oob_read_only",
    "main_read_only",
]


@dataclass(frozen=True)
class FoundationDashboardLayoutReadViewEntry:
    """Canonical layout read-view entry for foundation dashboard composition."""

    layout_entry_id: str
    panel_id: str
    display_title: str
    layout_zone: FoundationLayoutZone
    layout_order_index: int
    startup_stage_index: int
    left_menu_visible: bool
    center_visible: bool
    signal_path_visible: bool
    execution_stage_visible: bool
    view_mode: FoundationLayoutViewMode
    read_only: bool
    description: str


@dataclass(frozen=True)
class FoundationDashboardLayoutReadViewContract:
    """Canonical layout read-view contract for foundation dashboard composition."""

    total_entries: int
    left_menu_entries: int
    center_zone_entries: int
    ring_zone_entries: int
    signal_visible_entries: int
    execution_stage_visible_entries: int
    startup_order_valid_entries: int
    entries: tuple[FoundationDashboardLayoutReadViewEntry, ...]


def build_foundation_dashboard_layout_read_view_contract() -> (
    FoundationDashboardLayoutReadViewContract
):
    """Build canonical layout read-view contract for foundation dashboard composition."""
    entries = (
        FoundationDashboardLayoutReadViewEntry(
            layout_entry_id="foundationlayout_runtime_001",
            panel_id="panel_foundation_runtime_status_001",
            display_title="Runtime Core",
            layout_zone="center_core",
            layout_order_index=1,
            startup_stage_index=1,
            left_menu_visible=True,
            center_visible=True,
            signal_path_visible=True,
            execution_stage_visible=True,
            view_mode="oob_read_only",
            read_only=True,
            description=(
                "Central runtime core layout read-view entry for foundation "
                "dashboard composition."
            ),
        ),
        FoundationDashboardLayoutReadViewEntry(
            layout_entry_id="foundationlayout_guard_001",
            panel_id="panel_foundation_guard_status_001",
            display_title="Stop-Gate Watcher",
            layout_zone="inner_ring",
            layout_order_index=2,
            startup_stage_index=2,
            left_menu_visible=True,
            center_visible=False,
            signal_path_visible=True,
            execution_stage_visible=True,
            view_mode="oob_read_only",
            read_only=True,
            description=(
                "Inner ring layout read-view entry for stop-gate watcher."
            ),
        ),
        FoundationDashboardLayoutReadViewEntry(
            layout_entry_id="foundationlayout_core_guard_001",
            panel_id="panel_foundation_core_guard_status_001",
            display_title="Core Guard",
            layout_zone="inner_ring",
            layout_order_index=3,
            startup_stage_index=3,
            left_menu_visible=True,
            center_visible=False,
            signal_path_visible=True,
            execution_stage_visible=True,
            view_mode="oob_read_only",
            read_only=True,
            description=(
                "Inner ring layout read-view entry for core guard."
            ),
        ),
        FoundationDashboardLayoutReadViewEntry(
            layout_entry_id="foundationlayout_kernel_guard_001",
            panel_id="panel_foundation_kernel_guard_status_001",
            display_title="Kernel Watchdog",
            layout_zone="outer_ring",
            layout_order_index=4,
            startup_stage_index=4,
            left_menu_visible=True,
            center_visible=False,
            signal_path_visible=True,
            execution_stage_visible=True,
            view_mode="oob_read_only",
            read_only=True,
            description=(
                "Outer ring layout read-view entry for kernel watchdog."
            ),
        ),
    )

    startup_order_valid_entries = 0
    expected_stage = 1
    for entry in entries:
        if entry.startup_stage_index == expected_stage:
            startup_order_valid_entries += 1
        expected_stage += 1

    return FoundationDashboardLayoutReadViewContract(
        total_entries=len(entries),
        left_menu_entries=sum(1 for entry in entries if entry.left_menu_visible),
        center_zone_entries=sum(
            1 for entry in entries if entry.layout_zone == "center_core"
        ),
        ring_zone_entries=sum(
            1 for entry in entries if entry.layout_zone in {"inner_ring", "outer_ring"}
        ),
        signal_visible_entries=sum(
            1 for entry in entries if entry.signal_path_visible
        ),
        execution_stage_visible_entries=sum(
            1 for entry in entries if entry.execution_stage_visible
        ),
        startup_order_valid_entries=startup_order_valid_entries,
        entries=entries,
    )
