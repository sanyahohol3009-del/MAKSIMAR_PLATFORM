from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_live_operator_showcase_contract import (
    build_visual_first_live_operator_showcase_contract,
)


DemoReadyLiveOperatorMode = Literal[
    "first_demo_ready_live_operator",
]

DemoReadyLiveOperatorStatus = Literal[
    "demo_ready_live_operator_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstDemoReadyLiveOperatorEntry:
    """Canonical first demo-ready live operator entry."""

    demo_ready_live_operator_id: str
    live_operator_showcase_id: str
    demo_ready_live_operator_mode: DemoReadyLiveOperatorMode
    demo_ready_live_operator_status: DemoReadyLiveOperatorStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    live_operator_showcase_ready: bool
    demo_ready_live_operator_ready: bool
    truth_bound_demo_ready_live_operator: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstDemoReadyLiveOperatorContract:
    """Canonical first demo-ready live operator contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstDemoReadyLiveOperatorEntry, ...]


def build_visual_first_demo_ready_live_operator_contract(
) -> VisualFirstDemoReadyLiveOperatorContract:
    """Build canonical first demo-ready live operator contract."""
    live_operator_showcase_contract = (
        build_visual_first_live_operator_showcase_contract()
    )
    live_operator_showcase_entry = live_operator_showcase_contract.entries[0]

    entries = (
        VisualFirstDemoReadyLiveOperatorEntry(
            demo_ready_live_operator_id="visual_first_demo_ready_live_operator_001",
            live_operator_showcase_id=(
                live_operator_showcase_entry.live_operator_showcase_id
            ),
            demo_ready_live_operator_mode="first_demo_ready_live_operator",
            demo_ready_live_operator_status="demo_ready_live_operator_ready",
            renderer_surface_id=live_operator_showcase_entry.renderer_surface_id,
            theme_id=live_operator_showcase_entry.theme_id,
            screen_id=live_operator_showcase_entry.screen_id,
            preview_artifact_id=live_operator_showcase_entry.preview_artifact_id,
            live_operator_showcase_ready=(
                live_operator_showcase_entry.live_operator_showcase_ready
            ),
            demo_ready_live_operator_ready=True,
            truth_bound_demo_ready_live_operator=True,
            read_only=True,
            description=(
                "Canonical first demo-ready live operator entry after assembly "
                "of the first truth-preserving live operator showcase."
            ),
        ),
    )

    return VisualFirstDemoReadyLiveOperatorContract(
        contract_id="visual_first_demo_ready_live_operator_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.demo_ready_live_operator_status
            == "demo_ready_live_operator_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
