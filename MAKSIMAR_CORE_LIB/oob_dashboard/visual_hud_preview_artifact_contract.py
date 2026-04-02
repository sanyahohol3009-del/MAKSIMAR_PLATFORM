from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_render_result_contract import (
    build_visual_hud_render_result_contract,
)


ArtifactFormat = Literal[
    "hud_preview_bundle",
]

ArtifactState = Literal[
    "artifact_ready",
    "artifact_partial",
]


@dataclass(frozen=True, slots=True)
class VisualHudPreviewArtifactEntry:
    """Canonical HUD preview artifact entry for first artifact-ready preview output."""

    artifact_id: str
    render_result_id: str
    renderer_surface_id: str
    theme_id: str
    artifact_format: ArtifactFormat
    artifact_state: ArtifactState
    top_layer_id: str
    center_layer_id: str
    bottom_layer_id: str
    right_sidebar_layer_id: str
    total_layers: int
    visible_layers: int
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualHudPreviewArtifactContract:
    """Canonical HUD preview artifact contract for first artifact-ready preview output."""

    contract_id: str
    total_entries: int
    artifact_ready_entries: int
    artifact_partial_entries: int
    read_only_entries: int
    total_visible_layers: int
    entries: tuple[VisualHudPreviewArtifactEntry, ...]


def build_visual_hud_preview_artifact_contract() -> (
    VisualHudPreviewArtifactContract
):
    """Build canonical HUD preview artifact contract."""
    render_result_contract = build_visual_hud_render_result_contract()
    render_result_entry = render_result_contract.entries[0]

    artifact_state: ArtifactState = (
        "artifact_ready"
        if render_result_entry.render_state == "render_complete"
        else "artifact_partial"
    )

    entries = (
        VisualHudPreviewArtifactEntry(
            artifact_id="visual_hud_preview_artifact_001",
            render_result_id=render_result_entry.render_result_id,
            renderer_surface_id=render_result_entry.renderer_surface_id,
            theme_id=render_result_entry.theme_id,
            artifact_format="hud_preview_bundle",
            artifact_state=artifact_state,
            top_layer_id=render_result_entry.top_layer_id,
            center_layer_id=render_result_entry.center_layer_id,
            bottom_layer_id=render_result_entry.bottom_layer_id,
            right_sidebar_layer_id=render_result_entry.right_sidebar_layer_id,
            total_layers=render_result_entry.total_layers,
            visible_layers=render_result_entry.visible_layers,
            read_only=True,
            description=(
                "Canonical HUD preview artifact entry for first artifact-ready HUD output."
            ),
        ),
    )

    return VisualHudPreviewArtifactContract(
        contract_id="visual_hud_preview_artifact_contract_001",
        total_entries=len(entries),
        artifact_ready_entries=sum(
            1 for entry in entries if entry.artifact_state == "artifact_ready"
        ),
        artifact_partial_entries=sum(
            1 for entry in entries if entry.artifact_state == "artifact_partial"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        total_visible_layers=sum(entry.visible_layers for entry in entries),
        entries=entries,
    )
