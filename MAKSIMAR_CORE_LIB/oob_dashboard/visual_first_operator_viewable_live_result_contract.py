from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_live_showcase_result_contract import (
    build_visual_first_live_showcase_result_contract,
)


OperatorViewableLiveResultMode = Literal[
    "first_operator_viewable_live_result",
]

OperatorViewableLiveResultStatus = Literal[
    "operator_viewable_live_result_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstOperatorViewableLiveResultEntry:
    """Canonical first operator-viewable live result entry."""

    operator_viewable_live_result_id: str
    live_showcase_result_id: str
    operator_viewable_live_result_mode: OperatorViewableLiveResultMode
    operator_viewable_live_result_status: OperatorViewableLiveResultStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    live_showcase_result_ready: bool
    operator_viewable_live_result_ready: bool
    truth_bound_operator_viewable_live_result: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstOperatorViewableLiveResultContract:
    """Canonical first operator-viewable live result contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstOperatorViewableLiveResultEntry, ...]


def build_visual_first_operator_viewable_live_result_contract(
) -> VisualFirstOperatorViewableLiveResultContract:
    """Build canonical first operator-viewable live result contract."""
    live_showcase_result_contract = build_visual_first_live_showcase_result_contract()
    live_showcase_result_entry = live_showcase_result_contract.entries[0]

    entries = (
        VisualFirstOperatorViewableLiveResultEntry(
            operator_viewable_live_result_id=(
                "visual_first_operator_viewable_live_result_001"
            ),
            live_showcase_result_id=live_showcase_result_entry.live_showcase_result_id,
            operator_viewable_live_result_mode="first_operator_viewable_live_result",
            operator_viewable_live_result_status=(
                "operator_viewable_live_result_ready"
            ),
            renderer_surface_id=live_showcase_result_entry.renderer_surface_id,
            theme_id=live_showcase_result_entry.theme_id,
            screen_id=live_showcase_result_entry.screen_id,
            preview_artifact_id=live_showcase_result_entry.preview_artifact_id,
            live_showcase_result_ready=(
                live_showcase_result_entry.live_showcase_result_ready
            ),
            operator_viewable_live_result_ready=True,
            truth_bound_operator_viewable_live_result=True,
            read_only=True,
            description=(
                "Canonical first operator-viewable live result entry after "
                "assembly of the first truth-preserving live showcase result."
            ),
        ),
    )

    return VisualFirstOperatorViewableLiveResultContract(
        contract_id="visual_first_operator_viewable_live_result_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.operator_viewable_live_result_status
            == "operator_viewable_live_result_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
