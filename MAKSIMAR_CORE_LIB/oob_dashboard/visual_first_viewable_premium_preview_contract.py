from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_operator_facing_premium_preview_contract import (
    build_visual_operator_facing_premium_preview_contract,
)


FirstViewablePreviewMode = Literal[
    "first_viewable_premium_preview",
]

FirstViewablePreviewStatus = Literal[
    "viewable_preview_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstViewablePremiumPreviewEntry:
    """Canonical first viewable premium preview entry."""

    preview_id: str
    operator_preview_id: str
    preview_mode: FirstViewablePreviewMode
    preview_status: FirstViewablePreviewStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    operator_facing_ready: bool
    display_facing_ready: bool
    truth_bound_preview: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstViewablePremiumPreviewContract:
    """Canonical first viewable premium preview contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstViewablePremiumPreviewEntry, ...]


def build_visual_first_viewable_premium_preview_contract(
) -> VisualFirstViewablePremiumPreviewContract:
    """Build canonical first viewable premium preview contract."""
    operator_preview_contract = build_visual_operator_facing_premium_preview_contract()
    operator_preview_entry = operator_preview_contract.entries[0]

    entries = (
        VisualFirstViewablePremiumPreviewEntry(
            preview_id="visual_first_viewable_premium_preview_001",
            operator_preview_id=operator_preview_entry.preview_id,
            preview_mode="first_viewable_premium_preview",
            preview_status="viewable_preview_ready",
            renderer_surface_id=operator_preview_entry.renderer_surface_id,
            theme_id=operator_preview_entry.theme_id,
            screen_id=operator_preview_entry.screen_id,
            preview_artifact_id=operator_preview_entry.preview_artifact_id,
            operator_facing_ready=True,
            display_facing_ready=True,
            truth_bound_preview=True,
            read_only=True,
            description=(
                "Canonical first viewable premium preview entry after "
                "truth-preserving operator-facing premium preview assembly."
            ),
        ),
    )

    return VisualFirstViewablePremiumPreviewContract(
        contract_id="visual_first_viewable_premium_preview_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.preview_status == "viewable_preview_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
