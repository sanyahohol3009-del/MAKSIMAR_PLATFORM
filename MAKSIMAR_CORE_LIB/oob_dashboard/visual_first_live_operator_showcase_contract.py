from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_operator_viewable_live_result_contract import (
    build_visual_first_operator_viewable_live_result_contract,
)


LiveOperatorShowcaseMode = Literal[
    "first_live_operator_showcase",
]

LiveOperatorShowcaseStatus = Literal[
    "live_operator_showcase_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstLiveOperatorShowcaseEntry:
    """Canonical first live operator showcase entry."""

    live_operator_showcase_id: str
    operator_viewable_live_result_id: str
    live_operator_showcase_mode: LiveOperatorShowcaseMode
    live_operator_showcase_status: LiveOperatorShowcaseStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    operator_viewable_live_result_ready: bool
    live_operator_showcase_ready: bool
    truth_bound_live_operator_showcase: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstLiveOperatorShowcaseContract:
    """Canonical first live operator showcase contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstLiveOperatorShowcaseEntry, ...]


def build_visual_first_live_operator_showcase_contract(
) -> VisualFirstLiveOperatorShowcaseContract:
    """Build canonical first live operator showcase contract."""
    operator_viewable_live_result_contract = (
        build_visual_first_operator_viewable_live_result_contract()
    )
    operator_viewable_live_result_entry = (
        operator_viewable_live_result_contract.entries[0]
    )

    entries = (
        VisualFirstLiveOperatorShowcaseEntry(
            live_operator_showcase_id="visual_first_live_operator_showcase_001",
            operator_viewable_live_result_id=(
                operator_viewable_live_result_entry.operator_viewable_live_result_id
            ),
            live_operator_showcase_mode="first_live_operator_showcase",
            live_operator_showcase_status="live_operator_showcase_ready",
            renderer_surface_id=operator_viewable_live_result_entry.renderer_surface_id,
            theme_id=operator_viewable_live_result_entry.theme_id,
            screen_id=operator_viewable_live_result_entry.screen_id,
            preview_artifact_id=operator_viewable_live_result_entry.preview_artifact_id,
            operator_viewable_live_result_ready=(
                operator_viewable_live_result_entry.operator_viewable_live_result_ready
            ),
            live_operator_showcase_ready=True,
            truth_bound_live_operator_showcase=True,
            read_only=True,
            description=(
                "Canonical first live operator showcase entry after assembly "
                "of the first truth-preserving operator-viewable live result."
            ),
        ),
    )

    return VisualFirstLiveOperatorShowcaseContract(
        contract_id="visual_first_live_operator_showcase_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.live_operator_showcase_status
            == "live_operator_showcase_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
