from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_preview_render_artifact_bridge_contract import (
    build_visual_preview_render_artifact_bridge_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_preview_state_contract import (
    build_visual_hud_preview_state_contract,
)


DisplayFacingBundleMode = Literal[
    "display_facing_preview_bundle",
]

DisplayFacingBundleStatus = Literal[
    "bundle_ready",
]


@dataclass(frozen=True, slots=True)
class VisualDisplayFacingPreviewBundleEntry:
    """Canonical display-facing preview bundle entry."""

    bundle_id: str
    bridge_id: str
    preview_state_id: str
    bundle_mode: DisplayFacingBundleMode
    bundle_status: DisplayFacingBundleStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    display_facing_ready: bool
    truth_bound_bundle: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualDisplayFacingPreviewBundleContract:
    """Canonical display-facing preview bundle contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualDisplayFacingPreviewBundleEntry, ...]


def build_visual_display_facing_preview_bundle_contract(
) -> VisualDisplayFacingPreviewBundleContract:
    """Build canonical display-facing preview bundle contract."""
    artifact_bridge_contract = build_visual_preview_render_artifact_bridge_contract()
    preview_state_contract = build_visual_hud_preview_state_contract()

    artifact_bridge_entry = artifact_bridge_contract.entries[0]
    preview_state_entry = preview_state_contract.entries[0]

    entries = (
        VisualDisplayFacingPreviewBundleEntry(
            bundle_id="visual_display_facing_preview_bundle_001",
            bridge_id=artifact_bridge_entry.bridge_id,
            preview_state_id=preview_state_entry.preview_state_id,
            bundle_mode="display_facing_preview_bundle",
            bundle_status="bundle_ready",
            renderer_surface_id=artifact_bridge_entry.renderer_surface_id,
            theme_id=artifact_bridge_entry.theme_id,
            screen_id=artifact_bridge_entry.screen_id,
            preview_artifact_id=artifact_bridge_entry.preview_artifact_id,
            display_facing_ready=True,
            truth_bound_bundle=True,
            read_only=True,
            description=(
                "Canonical display-facing preview bundle entry for "
                "truth-preserving HUD preview delivery."
            ),
        ),
    )

    return VisualDisplayFacingPreviewBundleContract(
        contract_id="visual_display_facing_preview_bundle_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1 for entry in entries if entry.bundle_status == "bundle_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
