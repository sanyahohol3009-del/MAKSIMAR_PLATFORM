from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


FoundationVisualLayer = Literal[
    "central_core",
    "inner_guard_ring",
    "outer_guard_ring",
]

FoundationVisualAnchor = Literal[
    "center",
    "ring_inner_top",
    "ring_inner_right",
    "ring_outer_top",
]


@dataclass(frozen=True)
class FoundationVisualCompositionEntry:
    """Canonical visual composition entry for foundation dashboard structure."""

    composition_entry_id: str
    panel_id: str
    display_title: str
    visual_layer: FoundationVisualLayer
    visual_anchor: FoundationVisualAnchor
    startup_stage_index: int
    central_to_core_map: bool
    signal_path_visible: bool
    execution_stage_visible: bool
    show_in_oob_dashboard: bool
    show_in_main_dashboard: bool
    read_only: bool
    description: str


@dataclass(frozen=True)
class FoundationVisualCompositionContract:
    """Canonical visual composition contract for foundation dashboard structure."""

    total_entries: int
    central_core_entries: int
    inner_guard_entries: int
    outer_guard_entries: int
    signal_visible_entries: int
    execution_stage_visible_entries: int
    startup_order_valid_entries: int
    entries: tuple[FoundationVisualCompositionEntry, ...]


def build_foundation_visual_composition_contract() -> (
    FoundationVisualCompositionContract
):
    """Build canonical visual composition contract for foundation dashboard structure."""
    entries = (
        FoundationVisualCompositionEntry(
            composition_entry_id="foundationvisual_runtime_001",
            panel_id="panel_foundation_runtime_status_001",
            display_title="Runtime Core",
            visual_layer="central_core",
            visual_anchor="center",
            startup_stage_index=1,
            central_to_core_map=True,
            signal_path_visible=True,
            execution_stage_visible=True,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            read_only=True,
            description=(
                "Central core visual composition entry for runtime foundation state."
            ),
        ),
        FoundationVisualCompositionEntry(
            composition_entry_id="foundationvisual_guard_001",
            panel_id="panel_foundation_guard_status_001",
            display_title="Stop-Gate Watcher",
            visual_layer="inner_guard_ring",
            visual_anchor="ring_inner_top",
            startup_stage_index=2,
            central_to_core_map=True,
            signal_path_visible=True,
            execution_stage_visible=True,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            read_only=True,
            description=(
                "Inner guard ring visual composition entry for stop-gate watcher."
            ),
        ),
        FoundationVisualCompositionEntry(
            composition_entry_id="foundationvisual_core_guard_001",
            panel_id="panel_foundation_core_guard_status_001",
            display_title="Core Guard",
            visual_layer="inner_guard_ring",
            visual_anchor="ring_inner_right",
            startup_stage_index=3,
            central_to_core_map=True,
            signal_path_visible=True,
            execution_stage_visible=True,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            read_only=True,
            description=(
                "Inner guard ring visual composition entry for core guard."
            ),
        ),
        FoundationVisualCompositionEntry(
            composition_entry_id="foundationvisual_kernel_guard_001",
            panel_id="panel_foundation_kernel_guard_status_001",
            display_title="Kernel Watchdog",
            visual_layer="outer_guard_ring",
            visual_anchor="ring_outer_top",
            startup_stage_index=4,
            central_to_core_map=True,
            signal_path_visible=True,
            execution_stage_visible=True,
            show_in_oob_dashboard=True,
            show_in_main_dashboard=True,
            read_only=True,
            description=(
                "Outer guard ring visual composition entry for kernel watchdog."
            ),
        ),
    )

    startup_order_valid_entries = 0
    expected_stage = 1
    for entry in entries:
        if entry.startup_stage_index == expected_stage:
            startup_order_valid_entries += 1
        expected_stage += 1

    return FoundationVisualCompositionContract(
        total_entries=len(entries),
        central_core_entries=sum(
            1 for entry in entries if entry.visual_layer == "central_core"
        ),
        inner_guard_entries=sum(
            1 for entry in entries if entry.visual_layer == "inner_guard_ring"
        ),
        outer_guard_entries=sum(
            1 for entry in entries if entry.visual_layer == "outer_guard_ring"
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
