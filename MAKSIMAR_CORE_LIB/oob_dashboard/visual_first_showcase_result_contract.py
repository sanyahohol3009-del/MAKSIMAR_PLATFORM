from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_screen_result_contract import (
    build_visual_first_screen_result_contract,
)


ShowcaseResultMode = Literal[
    "first_showcase_result",
]

ShowcaseResultStatus = Literal[
    "showcase_result_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstShowcaseResultEntry:
    """Canonical first showcase result entry."""

    showcase_result_id: str
    screen_result_id: str
    showcase_result_mode: ShowcaseResultMode
    showcase_result_status: ShowcaseResultStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    screen_result_ready: bool
    showcase_result_ready: bool
    truth_bound_showcase_result: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstShowcaseResultContract:
    """Canonical first showcase result contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstShowcaseResultEntry, ...]


def build_visual_first_showcase_result_contract() -> VisualFirstShowcaseResultContract:
    """Build canonical first showcase result contract."""
    screen_result_contract = build_visual_first_screen_result_contract()
    screen_result_entry = screen_result_contract.entries[0]

    entries = (
        VisualFirstShowcaseResultEntry(
            showcase_result_id="visual_first_showcase_result_001",
            screen_result_id=screen_result_entry.screen_result_id,
            showcase_result_mode="first_showcase_result",
            showcase_result_status="showcase_result_ready",
            renderer_surface_id=screen_result_entry.renderer_surface_id,
            theme_id=screen_result_entry.theme_id,
            screen_id=screen_result_entry.screen_id,
            preview_artifact_id=screen_result_entry.preview_artifact_id,
            screen_result_ready=screen_result_entry.screen_result_ready,
            showcase_result_ready=True,
            truth_bound_showcase_result=True,
            read_only=True,
            description=(
                "Canonical first showcase result entry after assembly of the "
                "first truth-preserving screen result."
            ),
        ),
    )

    return VisualFirstShowcaseResultContract(
        contract_id="visual_first_showcase_result_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1 for entry in entries if entry.showcase_result_status == "showcase_result_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
