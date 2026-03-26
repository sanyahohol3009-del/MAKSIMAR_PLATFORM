from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


FoundationMenuSection = Literal[
    "foundation_core",
    "foundation_safety",
]

FoundationVisualRole = Literal[
    "central_core",
    "inner_guard_ring",
    "outer_guard_ring",
]

FoundationTruthScope = Literal[
    "runtime",
    "guard",
    "core_guard",
    "kernel_guard",
]


@dataclass(frozen=True)
class FoundationStatusReadModelEntry:
    """Canonical read-only dashboard read model entry for foundation surfaces."""

    read_model_entry_id: str
    panel_id: str
    menu_section: FoundationMenuSection
    menu_order_index: int
    display_title: str
    visual_role: FoundationVisualRole
    truth_scope: FoundationTruthScope
    startup_stage_index: int
    source_session_name: str
    source_status_command: str
    source_dashboard_window_name: str
    read_only: bool
    show_in_oob_dashboard: bool
    show_in_main_dashboard: bool
    central_to_core_map: bool
    signal_path_visible: bool
    execution_stage_visible: bool
    description: str


@dataclass(frozen=True)
class FoundationStatusReadModelContract:
    """Canonical read-only dashboard read model for foundation observability."""

    total_entries: int
    central_core_entries: int
    guard_ring_entries: int
    signal_visible_entries: int
    execution_stage_visible_entries: int
    startup_order_valid_entries: int
    entries: tuple[FoundationStatusReadModelEntry, ...]


def build_foundation_status_read_model_contract() -> (
    FoundationStatusReadModelContract
):
    """Build canonical read-only dashboard read model for foundation surfaces."""
    entries = (
        FoundationStatusReadModelEntry(
            read_model_entry_id="foundationreadmodel_runtime_001",
            panel_id="panel_foundation_runtime_status_001",
            menu_section="foundation_core",
            menu_order_index=1,
            display_title="Runtime Core",
            visual_role="central_core",
            truth_scope="runtime",
            startup_stage_index=1,
            source_session_name="maksimar",
            source_status_command="./tools/ctl status",
            source_dashboard_window_name="dash",
            read_only=True,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            central_to_core_map=True,
            signal_path_visible=True,
            execution_stage_visible=True,
            description=(
                "Central runtime core read model entry. Represents main alive state, "
                "health state, and core execution starting point."
            ),
        ),
        FoundationStatusReadModelEntry(
            read_model_entry_id="foundationreadmodel_guard_001",
            panel_id="panel_foundation_guard_status_001",
            menu_section="foundation_safety",
            menu_order_index=2,
            display_title="Stop-Gate Watcher",
            visual_role="inner_guard_ring",
            truth_scope="guard",
            startup_stage_index=2,
            source_session_name="maksimar_guard",
            source_status_command="./tools/guard_ctl status",
            source_dashboard_window_name="dash",
            read_only=True,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            central_to_core_map=True,
            signal_path_visible=True,
            execution_stage_visible=True,
            description=(
                "Inner safety ring read model entry for stop-gate watcher. Represents "
                "guard-stage signal continuity around runtime core."
            ),
        ),
        FoundationStatusReadModelEntry(
            read_model_entry_id="foundationreadmodel_core_guard_001",
            panel_id="panel_foundation_core_guard_status_001",
            menu_section="foundation_safety",
            menu_order_index=3,
            display_title="Core Guard",
            visual_role="inner_guard_ring",
            truth_scope="core_guard",
            startup_stage_index=3,
            source_session_name="maksimar_core_guard",
            source_status_command="./tools/core_guard_ctl status",
            source_dashboard_window_name="dash",
            read_only=True,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            central_to_core_map=True,
            signal_path_visible=True,
            execution_stage_visible=True,
            description=(
                "Inner safety ring read model entry for core guard. Represents core "
                "safety enforcement visibility around runtime core."
            ),
        ),
        FoundationStatusReadModelEntry(
            read_model_entry_id="foundationreadmodel_kernel_guard_001",
            panel_id="panel_foundation_kernel_guard_status_001",
            menu_section="foundation_safety",
            menu_order_index=4,
            display_title="Kernel Watchdog",
            visual_role="outer_guard_ring",
            truth_scope="kernel_guard",
            startup_stage_index=4,
            source_session_name="maksimar_kernel_guard",
            source_status_command="./tools/kernel_guard_ctl status",
            source_dashboard_window_name="dash",
            read_only=True,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            central_to_core_map=True,
            signal_path_visible=True,
            execution_stage_visible=True,
            description=(
                "Outer safety ring read model entry for kernel watchdog. Represents "
                "outer supervisory guard visibility around the full foundation."
            ),
        ),
    )

    startup_order_valid_entries = 0
    expected_stage = 1
    for entry in entries:
        if entry.startup_stage_index == expected_stage:
            startup_order_valid_entries += 1
        expected_stage += 1

    return FoundationStatusReadModelContract(
        total_entries=len(entries),
        central_core_entries=sum(
            1 for entry in entries if entry.visual_role == "central_core"
        ),
        guard_ring_entries=sum(
            1
            for entry in entries
            if entry.visual_role in {"inner_guard_ring", "outer_guard_ring"}
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
