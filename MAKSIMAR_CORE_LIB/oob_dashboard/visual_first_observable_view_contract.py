from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_showable_view_contract import (
    build_visual_first_showable_view_contract,
)


ObservableViewMode = Literal[
    "first_observable_view",
]

ObservableViewStatus = Literal[
    "observable_view_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstObservableViewEntry:
    """Canonical first observable view entry."""

    observable_view_id: str
    showable_view_id: str
    observable_view_mode: ObservableViewMode
    observable_view_status: ObservableViewStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    showable_ready: bool
    observable_ready: bool
    truth_bound_observable_view: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstObservableViewContract:
    """Canonical first observable view contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstObservableViewEntry, ...]


def build_visual_first_observable_view_contract(
) -> VisualFirstObservableViewContract:
    """Build canonical first observable view contract."""
    showable_view_contract = build_visual_first_showable_view_contract()
    showable_view_entry = showable_view_contract.entries[0]

    entries = (
        VisualFirstObservableViewEntry(
            observable_view_id="visual_first_observable_view_001",
            showable_view_id=showable_view_entry.showable_view_id,
            observable_view_mode="first_observable_view",
            observable_view_status="observable_view_ready",
            renderer_surface_id=showable_view_entry.renderer_surface_id,
            theme_id=showable_view_entry.theme_id,
            screen_id=showable_view_entry.screen_id,
            preview_artifact_id=showable_view_entry.preview_artifact_id,
            showable_ready=showable_view_entry.showable_ready,
            observable_ready=True,
            truth_bound_observable_view=True,
            read_only=True,
            description=(
                "Canonical first observable view entry after assembly of the "
                "first truth-preserving showable view."
            ),
        ),
    )

    return VisualFirstObservableViewContract(
        contract_id="visual_first_observable_view_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.observable_view_status == "observable_view_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
