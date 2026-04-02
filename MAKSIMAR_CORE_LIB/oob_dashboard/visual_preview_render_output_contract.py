from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_preview_artifact_contract import (
    build_visual_hud_preview_artifact_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_render_result_contract import (
    build_visual_hud_render_result_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_preview_render_polish_readiness_contract import (
    build_visual_preview_render_polish_readiness_contract,
)


PreviewRenderOutputMode = Literal[
    "phase_1_preview_render_output",
]

PreviewRenderOutputStatus = Literal[
    "output_ready",
]


@dataclass(frozen=True, slots=True)
class VisualPreviewRenderOutputEntry:
    """Canonical preview/render output entry after Phase 1 readiness."""

    output_id: str
    readiness_id: str
    render_result_id: str
    output_mode: PreviewRenderOutputMode
    output_status: PreviewRenderOutputStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    stable_output: bool
    truth_bound_output: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualPreviewRenderOutputContract:
    """Canonical preview/render output contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualPreviewRenderOutputEntry, ...]


def build_visual_preview_render_output_contract(
) -> VisualPreviewRenderOutputContract:
    """Build canonical preview/render output contract."""
    readiness_contract = build_visual_preview_render_polish_readiness_contract()
    render_result_contract = build_visual_hud_render_result_contract()
    preview_artifact_contract = build_visual_hud_preview_artifact_contract()

    readiness_entry = readiness_contract.entries[0]
    render_result_entry = render_result_contract.entries[0]
    preview_artifact_entry = preview_artifact_contract.entries[0]

    entries = (
        VisualPreviewRenderOutputEntry(
            output_id="visual_preview_render_output_001",
            readiness_id=readiness_entry.readiness_id,
            render_result_id=render_result_entry.render_result_id,
            output_mode="phase_1_preview_render_output",
            output_status="output_ready",
            renderer_surface_id=render_result_entry.renderer_surface_id,
            theme_id=render_result_entry.theme_id,
            screen_id=render_result_entry.screen_id,
            preview_artifact_id=preview_artifact_entry.artifact_id,
            stable_output=True,
            truth_bound_output=True,
            read_only=True,
            description=(
                "Canonical preview/render output entry after completion of "
                "Phase 1 readiness and render-result stabilization."
            ),
        ),
    )

    return VisualPreviewRenderOutputContract(
        contract_id="visual_preview_render_output_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1 for entry in entries if entry.output_status == "output_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
