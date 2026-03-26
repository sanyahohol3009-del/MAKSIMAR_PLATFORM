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
class FoundationStatusMenuRegistryEntry:
    """Canonical menu-registry entry for foundation status panels."""

    registry_entry_id: str
    panel_id: str
    menu_item_id: str
    menu_section: FoundationMenuSection
    menu_order_index: int
    menu_label: str
    short_status_label: str
    visual_role: FoundationVisualRole
    show_in_left_menu: bool
    show_in_oob_dashboard: bool
    show_in_main_dashboard: bool
    read_only: bool
    operator_actions_allowed: bool
    startup_stage_index: int
    description: str


@dataclass(frozen=True)
class FoundationStatusMenuRegistryContract:
    """Canonical menu-registry contract for foundation status panels."""

    total_entries: int
    left_menu_entries: int
    oob_visible_entries: int
    main_dashboard_visible_entries: int
    read_only_entries: int
    startup_order_valid_entries: int
    entries: tuple[FoundationStatusMenuRegistryEntry, ...]


def build_foundation_status_menu_registry_contract() -> (
    FoundationStatusMenuRegistryContract
):
    """Build canonical menu-registry contract for foundation status panels."""
    entries = (
        FoundationStatusMenuRegistryEntry(
            registry_entry_id="foundationmenuregistry_runtime_001",
            panel_id="panel_foundation_runtime_status_001",
            menu_item_id="menu_foundation_runtime_001",
            menu_section="foundation_core",
            menu_order_index=1,
            menu_label="Runtime Core",
            short_status_label="RUNTIME",
            visual_role="central_core",
            show_in_left_menu=True,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            read_only=True,
            operator_actions_allowed=False,
            startup_stage_index=1,
            description=(
                "Canonical menu-registry entry for runtime core foundation panel."
            ),
        ),
        FoundationStatusMenuRegistryEntry(
            registry_entry_id="foundationmenuregistry_guard_001",
            panel_id="panel_foundation_guard_status_001",
            menu_item_id="menu_foundation_guard_001",
            menu_section="foundation_safety",
            menu_order_index=2,
            menu_label="Stop-Gate Watcher",
            short_status_label="STOP-GATE",
            visual_role="inner_guard_ring",
            show_in_left_menu=True,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            read_only=True,
            operator_actions_allowed=False,
            startup_stage_index=2,
            description=(
                "Canonical menu-registry entry for stop-gate watcher foundation panel."
            ),
        ),
        FoundationStatusMenuRegistryEntry(
            registry_entry_id="foundationmenuregistry_core_guard_001",
            panel_id="panel_foundation_core_guard_status_001",
            menu_item_id="menu_foundation_core_guard_001",
            menu_section="foundation_safety",
            menu_order_index=3,
            menu_label="Core Guard",
            short_status_label="CORE-GUARD",
            visual_role="inner_guard_ring",
            show_in_left_menu=True,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            read_only=True,
            operator_actions_allowed=False,
            startup_stage_index=3,
            description=(
                "Canonical menu-registry entry for core guard foundation panel."
            ),
        ),
        FoundationStatusMenuRegistryEntry(
            registry_entry_id="foundationmenuregistry_kernel_guard_001",
            panel_id="panel_foundation_kernel_guard_status_001",
            menu_item_id="menu_foundation_kernel_guard_001",
            menu_section="foundation_safety",
            menu_order_index=4,
            menu_label="Kernel Watchdog",
            short_status_label="KERNEL",
            visual_role="outer_guard_ring",
            show_in_left_menu=True,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            read_only=True,
            operator_actions_allowed=False,
            startup_stage_index=4,
            description=(
                "Canonical menu-registry entry for kernel watchdog foundation panel."
            ),
        ),
    )

    startup_order_valid_entries = 0
    expected_stage = 1
    for entry in entries:
        if entry.startup_stage_index == expected_stage:
            startup_order_valid_entries += 1
        expected_stage += 1

    return FoundationStatusMenuRegistryContract(
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
