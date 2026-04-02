from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_display_facing_preview_bundle_contract import (
    build_visual_display_facing_preview_bundle_contract,
)


OperatorFacingPreviewMode = Literal[
    "operator_facing_premium_preview",
]

OperatorFacingPreviewStatus = Literal[
    "premium_preview_ready",
]

PremiumPreviewProfile = Literal[
    "phase_1_premium_operator_hud",
]


@dataclass(frozen=True, slots=True)
class VisualOperatorFacingPremiumPreviewEntry:
    """Canonical operator-facing premium preview entry."""

    preview_id: str
    display_bundle_id: str
    preview_mode: OperatorFacingPreviewMode
    preview_status: OperatorFacingPreviewStatus
    premium_preview_profile: PremiumPreviewProfile
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    stronger_center_core_presentation: bool
    stronger_panel_hierarchy_presentation: bool
    stronger_sidebar_navigation_presentation: bool
    stronger_status_ticker_presentation: bool
    truth_bound_preview: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualOperatorFacingPremiumPreviewContract:
    """Canonical operator-facing premium preview contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualOperatorFacingPremiumPreviewEntry, ...]


def build_visual_operator_facing_premium_preview_contract(
) -> VisualOperatorFacingPremiumPreviewContract:
    """Build canonical operator-facing premium preview contract."""
    display_bundle_contract = build_visual_display_facing_preview_bundle_contract()
    display_bundle_entry = display_bundle_contract.entries[0]

    entries = (
        VisualOperatorFacingPremiumPreviewEntry(
            preview_id="visual_operator_facing_premium_preview_001",
            display_bundle_id=display_bundle_entry.bundle_id,
            preview_mode="operator_facing_premium_preview",
            preview_status="premium_preview_ready",
            premium_preview_profile="phase_1_premium_operator_hud",
            renderer_surface_id=display_bundle_entry.renderer_surface_id,
            theme_id=display_bundle_entry.theme_id,
            screen_id=display_bundle_entry.screen_id,
            preview_artifact_id=display_bundle_entry.preview_artifact_id,
            stronger_center_core_presentation=True,
            stronger_panel_hierarchy_presentation=True,
            stronger_sidebar_navigation_presentation=True,
            stronger_status_ticker_presentation=True,
            truth_bound_preview=True,
            read_only=True,
            description=(
                "Canonical operator-facing premium preview entry for "
                "truth-preserving Phase 1 HUD presentation."
            ),
        ),
    )

    return VisualOperatorFacingPremiumPreviewContract(
        contract_id="visual_operator_facing_premium_preview_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.preview_status == "premium_preview_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
