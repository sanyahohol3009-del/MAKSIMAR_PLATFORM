from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


FoundationTruthScope = Literal[
    "runtime",
    "guard",
    "core_guard",
    "kernel_guard",
]


@dataclass(frozen=True)
class FoundationStatusDashboardBridgeEntry:
    """Read-only bridge entry from foundation status surfaces into dashboard systems."""

    bridge_entry_id: str
    status_surface_id: str
    panel_id: str
    menu_label: str
    linked_session_name: str
    status_command: str
    dashboard_window_name: str
    truth_scope: FoundationTruthScope
    startup_stage_index: int
    show_in_oob_dashboard: bool
    show_in_main_dashboard: bool
    read_only: bool
    operator_actions_allowed: bool
    status_surface_contract_id: str
    description: str


@dataclass(frozen=True)
class FoundationStatusDashboardBridgeContract:
    """Canonical read-only bridge contract for foundation status surfaces."""

    total_entries: int
    read_only_entries: int
    oob_visible_entries: int
    main_dashboard_visible_entries: int
    startup_order_valid_entries: int
    entries: tuple[FoundationStatusDashboardBridgeEntry, ...]


def build_foundation_status_dashboard_bridge_contract() -> (
    FoundationStatusDashboardBridgeContract
):
    """Build canonical foundation status dashboard bridge contract."""
    entries = (
        FoundationStatusDashboardBridgeEntry(
            bridge_entry_id="foundationbridge_runtime_001",
            status_surface_id="statussurface_runtime_001",
            panel_id="panel_foundation_runtime_status_001",
            menu_label="Foundation Runtime",
            linked_session_name="maksimar",
            status_command="./tools/ctl status",
            dashboard_window_name="dash",
            truth_scope="runtime",
            startup_stage_index=1,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            read_only=True,
            operator_actions_allowed=False,
            status_surface_contract_id="STATUS_SURFACE_CONTRACT_v1",
            description=(
                "Canonical read-only runtime status bridge entry for current "
                "foundation observability shell."
            ),
        ),
        FoundationStatusDashboardBridgeEntry(
            bridge_entry_id="foundationbridge_guard_001",
            status_surface_id="statussurface_guard_001",
            panel_id="panel_foundation_guard_status_001",
            menu_label="Foundation Stop-Gate Watcher",
            linked_session_name="maksimar_guard",
            status_command="./tools/guard_ctl status",
            dashboard_window_name="dash",
            truth_scope="guard",
            startup_stage_index=2,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            read_only=True,
            operator_actions_allowed=False,
            status_surface_contract_id="STATUS_SURFACE_CONTRACT_v1",
            description=(
                "Canonical read-only stop-gate watcher status bridge entry for "
                "current foundation observability shell."
            ),
        ),
        FoundationStatusDashboardBridgeEntry(
            bridge_entry_id="foundationbridge_core_guard_001",
            status_surface_id="statussurface_core_guard_001",
            panel_id="panel_foundation_core_guard_status_001",
            menu_label="Foundation Core Guard",
            linked_session_name="maksimar_core_guard",
            status_command="./tools/core_guard_ctl status",
            dashboard_window_name="dash",
            truth_scope="core_guard",
            startup_stage_index=3,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            read_only=True,
            operator_actions_allowed=False,
            status_surface_contract_id="STATUS_SURFACE_CONTRACT_v1",
            description=(
                "Canonical read-only core guard status bridge entry for current "
                "foundation observability shell."
            ),
        ),
        FoundationStatusDashboardBridgeEntry(
            bridge_entry_id="foundationbridge_kernel_guard_001",
            status_surface_id="statussurface_kernel_guard_001",
            panel_id="panel_foundation_kernel_guard_status_001",
            menu_label="Foundation Kernel Watchdog",
            linked_session_name="maksimar_kernel_guard",
            status_command="./tools/kernel_guard_ctl status",
            dashboard_window_name="dash",
            truth_scope="kernel_guard",
            startup_stage_index=4,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            read_only=True,
            operator_actions_allowed=False,
            status_surface_contract_id="STATUS_SURFACE_CONTRACT_v1",
            description=(
                "Canonical read-only kernel watchdog status bridge entry for "
                "current foundation observability shell."
            ),
        ),
    )

    startup_order_valid_entries = 0
    expected_stage = 1
    for entry in entries:
        if entry.startup_stage_index == expected_stage:
            startup_order_valid_entries += 1
        expected_stage += 1

    return FoundationStatusDashboardBridgeContract(
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        oob_visible_entries=sum(
            1 for entry in entries if entry.show_in_oob_dashboard
        ),
        main_dashboard_visible_entries=sum(
            1 for entry in entries if entry.show_in_main_dashboard
        ),
        startup_order_valid_entries=startup_order_valid_entries,
        entries=entries,
    )
