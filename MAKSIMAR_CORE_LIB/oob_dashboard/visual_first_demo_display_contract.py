from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_presentable_display_contract import (
    build_visual_first_presentable_display_contract,
)


DemoDisplayMode = Literal[
    "first_demo_display",
]

DemoDisplayStatus = Literal[
    "demo_display_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstDemoDisplayEntry:
    """Canonical first demo display entry."""

    demo_display_id: str
    presentable_display_id: str
    demo_display_mode: DemoDisplayMode
    demo_display_status: DemoDisplayStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    presentable_display_ready: bool
    demo_display_ready: bool
    truth_bound_demo_display: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstDemoDisplayContract:
    """Canonical first demo display contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstDemoDisplayEntry, ...]


def build_visual_first_demo_display_contract() -> VisualFirstDemoDisplayContract:
    """Build canonical first demo display contract."""
    presentable_display_contract = build_visual_first_presentable_display_contract()
    presentable_display_entry = presentable_display_contract.entries[0]

    entries = (
        VisualFirstDemoDisplayEntry(
            demo_display_id="visual_first_demo_display_001",
            presentable_display_id=presentable_display_entry.display_id,
            demo_display_mode="first_demo_display",
            demo_display_status="demo_display_ready",
            renderer_surface_id=presentable_display_entry.renderer_surface_id,
            theme_id=presentable_display_entry.theme_id,
            screen_id=presentable_display_entry.screen_id,
            preview_artifact_id=presentable_display_entry.preview_artifact_id,
            presentable_display_ready=presentable_display_entry.presentable_display_ready,
            demo_display_ready=True,
            truth_bound_demo_display=True,
            read_only=True,
            description=(
                "Canonical first demo display entry after assembly of the "
                "first truth-preserving presentable display."
            ),
        ),
    )

    return VisualFirstDemoDisplayContract(
        contract_id="visual_first_demo_display_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1 for entry in entries if entry.demo_display_status == "demo_display_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
