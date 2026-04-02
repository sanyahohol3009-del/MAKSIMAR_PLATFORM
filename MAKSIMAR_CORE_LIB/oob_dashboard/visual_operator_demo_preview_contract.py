from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_presentable_preview_contract import (
    build_visual_first_presentable_preview_contract,
)


OperatorDemoPreviewMode = Literal[
    "operator_demo_preview",
]

OperatorDemoPreviewStatus = Literal[
    "demo_preview_ready",
]


@dataclass(frozen=True, slots=True)
class VisualOperatorDemoPreviewEntry:
    """Canonical operator demo preview entry."""

    preview_id: str
    presentable_preview_id: str
    preview_mode: OperatorDemoPreviewMode
    preview_status: OperatorDemoPreviewStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    presentable_ready: bool
    operator_demo_ready: bool
    truth_bound_preview: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualOperatorDemoPreviewContract:
    """Canonical operator demo preview contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualOperatorDemoPreviewEntry, ...]


def build_visual_operator_demo_preview_contract(
) -> VisualOperatorDemoPreviewContract:
    """Build canonical operator demo preview contract."""
    presentable_contract = build_visual_first_presentable_preview_contract()
    presentable_entry = presentable_contract.entries[0]

    entries = (
        VisualOperatorDemoPreviewEntry(
            preview_id="visual_operator_demo_preview_001",
            presentable_preview_id=presentable_entry.preview_id,
            preview_mode="operator_demo_preview",
            preview_status="demo_preview_ready",
            renderer_surface_id=presentable_entry.renderer_surface_id,
            theme_id=presentable_entry.theme_id,
            screen_id=presentable_entry.screen_id,
            preview_artifact_id=presentable_entry.preview_artifact_id,
            presentable_ready=presentable_entry.presentable_ready,
            operator_demo_ready=True,
            truth_bound_preview=True,
            read_only=True,
            description=(
                "Canonical operator demo preview entry after first "
                "presentable truth-preserving premium preview."
            ),
        ),
    )

    return VisualOperatorDemoPreviewContract(
        contract_id="visual_operator_demo_preview_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1 for entry in entries if entry.preview_status == "demo_preview_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
