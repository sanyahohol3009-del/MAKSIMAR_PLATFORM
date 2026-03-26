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


@dataclass(frozen=True)
class FoundationStatusPanelSummaryEntry:
    """Canonical summary entry for foundation panels in dashboard systems."""

    summary_entry_id: str
    panel_id: str
    menu_section: FoundationMenuSection
    menu_order_index: int
    display_title: str
    short_status_label: str
    visual_role: FoundationVisualRole
    source_status_command: str
    source_session_name: str
    startup_stage_index: int
    show_in_left_menu: bool
    show_in_oob_dashboard: bool
    show_in_main_dashboard: bool
    read_only: bool
    operator_actions_allowed: bool
    signal_path_visible: bool
    execution_stage_visible: bool
    description: str


@dataclass(frozen=True)
class FoundationStatusPanelSummaryContract:
    """Canonical panel summary contract for foundation dashboard entries."""

    total_entries: int
    left_menu_entries: int
    oob_visible_entries: int
    main_dashboard_visible_entries: int
    read_only_entries: int
    startup_order_valid_entries: int
    entries: tuple[FoundationStatusPanelSummaryEntry, ...]


def build_foundation_status_panel_summary_contract() -> (
    FoundationStatusPanelSummaryContract
):
    """Build canonical panel summary contract for foundation dashboard entries."""
    entries = (
        FoundationStatusPanelSummaryEntry(
            summary_entry_id="foundationsummary_runtime_001",
            panel_id="panel_foundation_runtime_status_001",
            menu_section="foundation_core",
            menu_order_index=1,
            display_title="Runtime Core",
            short_status_label="RUNTIME",
            visual_role="central_core",
            source_status_command="./tools/ctl status",
            source_session_name="maksimar",
            startup_stage_index=1,
            show_in_left_menu=True,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            read_only=True,
            operator_actions_allowed=False,
            signal_path_visible=True,
            execution_stage_visible=True,
            description=(
                "Canonical summary entry for runtime core panel in foundation "
                "dashboard systems."
            ),
        ),
        FoundationStatusPanelSummaryEntry(
            summary_entry_id="foundationsummary_guard_001",
            panel_id="panel_foundation_guard_status_001",
            menu_section="foundation_safety",
            menu_order_index=2,
            display_title="Stop-Gate Watcher",
            short_status_label="STOP-GATE",
            visual_role="inner_guard_ring",
            source_status_command="./tools/guard_ctl status",
            source_session_name="maksimar_guard",
            startup_stage_index=2,
            show_in_left_menu=True,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            read_only=True,
            operator_actions_allowed=False,
            signal_path_visible=True,
            execution_stage_visible=True,
            description=(
                "Canonical summary entry for stop-gate watcher panel in foundation "
                "dashboard systems."
            ),
        ),
        FoundationStatusPanelSummaryEntry(
            summary_entry_id="foundationsummary_core_guard_001",
            panel_id="panel_foundation_core_guard_status_001",
            menu_section="foundation_safety",
            menu_order_index=3,
            display_title="Core Guard",
            short_status_label="CORE-GUARD",
            visual_role="inner_guard_ring",
            source_status_command="./tools/core_guard_ctl status",
            source_session_name="maksimar_core_guard",
            startup_stage_index=3,
            show_in_left_menu=True,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            read_only=True,
            operator_actions_allowed=False,
            signal_path_visible=True,
            execution_stage_visible=True,
            description=(
                "Canonical summary entry for core guard panel in foundation "
                "dashboard systems."
            ),
        ),
        FoundationStatusPanelSummaryEntry(
            summary_entry_id="foundationsummary_kernel_guard_001",
            panel_id="panel_foundation_kernel_guard_status_001",
            menu_section="foundation_safety",
            menu_order_index=4,
            display_title="Kernel Watchdog",
            short_status_label="KERNEL",
            visual_role="outer_guard_ring",
            source_status_command="./tools/kernel_guard_ctl status",
            source_session_name="maksimar_kernel_guard",
            startup_stage_index=4,
            show_in_left_menu=True,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            read_only=True,
            operator_actions_allowed=False,
            signal_path_visible=True,
            execution_stage_visible=True,
            description=(
                "Canonical summary entry for kernel watchdog panel in foundation "
                "dashboard systems."
            ),
        ),
    )

    startup_order_valid_entries = 0
    expected_stage = 1
    for entry in entries:
        if entry.startup_stage_index == expected_stage:
            startup_order_valid_entries += 1
        expected_stage += 1

    return FoundationStatusPanelSummaryContract(
        total_entries=len(entries),
        left_menu_entries=sum(1 for entry in entries if entry.show_in_left_menu),
        oob_visible_entries=sum(
            1 for entry in entries if entry.show_in_oob_dashboard
        ),
        main_dashboard_visible_entries=sum(
            1 for entry in entries if entry.show_in_main_dashboard
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        startup_order_valid_entries=startup_order_valid_entries,
        entries=entries,
    )
