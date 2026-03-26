from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


FoundationWorkspaceZone = Literal[
    "left_menu",
    "center_core",
    "inner_ring",
    "outer_ring",
]

FoundationWorkspaceMode = Literal[
    "oob_read_only",
    "main_read_only",
]


@dataclass(frozen=True)
class FoundationDashboardWorkspaceEntry:
    """Canonical workspace entry for foundation dashboard composition."""

    workspace_entry_id: str
    panel_id: str
    zone_id: FoundationWorkspaceZone
    zone_order_index: int
    panel_order_index: int
    display_title: str
    startup_stage_index: int
    left_menu_visible: bool
    signal_path_visible: bool
    execution_stage_visible: bool
    workspace_mode: FoundationWorkspaceMode
    read_only: bool
    description: str


@dataclass(frozen=True)
class FoundationDashboardWorkspaceContract:
    """Canonical workspace contract for foundation dashboard composition."""

    workspace_id: str
    workspace_title: str
    total_entries: int
    left_menu_entries: int
    center_core_entries: int
    inner_ring_entries: int
    outer_ring_entries: int
    signal_visible_entries: int
    execution_stage_visible_entries: int
    startup_order_valid_entries: int
    entries: tuple[FoundationDashboardWorkspaceEntry, ...]


def build_foundation_dashboard_workspace_contract() -> (
    FoundationDashboardWorkspaceContract
):
    """Build canonical workspace contract for foundation dashboard composition."""
    entries = (
        FoundationDashboardWorkspaceEntry(
            workspace_entry_id="foundationworkspace_runtime_001",
            panel_id="panel_foundation_runtime_status_001",
            zone_id="center_core",
            zone_order_index=2,
            panel_order_index=1,
            display_title="Runtime Core",
            startup_stage_index=1,
            left_menu_visible=True,
            signal_path_visible=True,
            execution_stage_visible=True,
            workspace_mode="oob_read_only",
            read_only=True,
            description=(
                "Canonical center-core workspace entry for runtime foundation panel."
            ),
        ),
        FoundationDashboardWorkspaceEntry(
            workspace_entry_id="foundationworkspace_guard_001",
            panel_id="panel_foundation_guard_status_001",
            zone_id="inner_ring",
            zone_order_index=3,
            panel_order_index=2,
            display_title="Stop-Gate Watcher",
            startup_stage_index=2,
            left_menu_visible=True,
            signal_path_visible=True,
            execution_stage_visible=True,
            workspace_mode="oob_read_only",
            read_only=True,
            description=(
                "Canonical inner-ring workspace entry for stop-gate watcher panel."
            ),
        ),
        FoundationDashboardWorkspaceEntry(
            workspace_entry_id="foundationworkspace_core_guard_001",
            panel_id="panel_foundation_core_guard_status_001",
            zone_id="inner_ring",
            zone_order_index=3,
            panel_order_index=3,
            display_title="Core Guard",
            startup_stage_index=3,
            left_menu_visible=True,
            signal_path_visible=True,
            execution_stage_visible=True,
            workspace_mode="oob_read_only",
            read_only=True,
            description=(
                "Canonical inner-ring workspace entry for core guard panel."
            ),
        ),
        FoundationDashboardWorkspaceEntry(
            workspace_entry_id="foundationworkspace_kernel_guard_001",
            panel_id="panel_foundation_kernel_guard_status_001",
            zone_id="outer_ring",
            zone_order_index=4,
            panel_order_index=4,
            display_title="Kernel Watchdog",
            startup_stage_index=4,
            left_menu_visible=True,
            signal_path_visible=True,
            execution_stage_visible=True,
            workspace_mode="oob_read_only",
            read_only=True,
            description=(
                "Canonical outer-ring workspace entry for kernel watchdog panel."
            ),
        ),
    )

    startup_order_valid_entries = 0
    expected_stage = 1
    for entry in entries:
        if entry.startup_stage_index == expected_stage:
            startup_order_valid_entries += 1
        expected_stage += 1

    return FoundationDashboardWorkspaceContract(
        workspace_id="workspace_foundation_dashboard_001",
        workspace_title="Foundation Dashboard Workspace",
        total_entries=len(entries),
        left_menu_entries=sum(1 for entry in entries if entry.left_menu_visible),
        center_core_entries=sum(1 for entry in entries if entry.zone_id == "center_core"),
        inner_ring_entries=sum(1 for entry in entries if entry.zone_id == "inner_ring"),
        outer_ring_entries=sum(1 for entry in entries if entry.zone_id == "outer_ring"),
        signal_visible_entries=sum(1 for entry in entries if entry.signal_path_visible),
        execution_stage_visible_entries=sum(
            1 for entry in entries if entry.execution_stage_visible
        ),
        startup_order_valid_entries=startup_order_valid_entries,
        entries=entries,
    )
