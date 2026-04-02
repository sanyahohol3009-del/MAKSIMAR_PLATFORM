from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_preview_artifact_contract import (
    build_visual_hud_preview_artifact_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_preview_render_output_contract import (
    build_visual_preview_render_output_contract,
)


ArtifactBridgeMode = Literal[
    "preview_render_artifact_bridge",
]

ArtifactBridgeStatus = Literal[
    "bridge_ready",
]


@dataclass(frozen=True, slots=True)
class VisualPreviewRenderArtifactBridgeEntry:
    """Canonical bridge entry between preview/render output and preview artifact."""

    bridge_id: str
    output_id: str
    preview_artifact_id: str
    bridge_mode: ArtifactBridgeMode
    bridge_status: ArtifactBridgeStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    artifact_state: str
    truth_bound_bridge: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualPreviewRenderArtifactBridgeContract:
    """Canonical bridge contract between preview/render output and preview artifact."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualPreviewRenderArtifactBridgeEntry, ...]


def build_visual_preview_render_artifact_bridge_contract(
) -> VisualPreviewRenderArtifactBridgeContract:
    """Build canonical preview/render artifact bridge contract."""
    output_contract = build_visual_preview_render_output_contract()
    preview_artifact_contract = build_visual_hud_preview_artifact_contract()

    output_entry = output_contract.entries[0]
    preview_artifact_entry = preview_artifact_contract.entries[0]

    entries = (
        VisualPreviewRenderArtifactBridgeEntry(
            bridge_id="visual_preview_render_artifact_bridge_001",
            output_id=output_entry.output_id,
            preview_artifact_id=preview_artifact_entry.artifact_id,
            bridge_mode="preview_render_artifact_bridge",
            bridge_status="bridge_ready",
            renderer_surface_id=output_entry.renderer_surface_id,
            theme_id=output_entry.theme_id,
            screen_id=output_entry.screen_id,
            artifact_state=preview_artifact_entry.artifact_state,
            truth_bound_bridge=True,
            read_only=True,
            description=(
                "Canonical bridge entry between preview/render output and "
                "preview artifact for truth-preserving visual delivery."
            ),
        ),
    )

    return VisualPreviewRenderArtifactBridgeContract(
        contract_id="visual_preview_render_artifact_bridge_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1 for entry in entries if entry.bridge_status == "bridge_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
