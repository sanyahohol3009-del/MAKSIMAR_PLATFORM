from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_preview_delivery_readiness_contract import (
    build_visual_preview_delivery_readiness_contract,
)


FirstPresentablePreviewMode = Literal[
    "first_presentable_preview",
]

FirstPresentablePreviewStatus = Literal[
    "presentable_preview_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstPresentablePreviewEntry:
    """Canonical first presentable preview entry."""

    preview_id: str
    delivery_readiness_id: str
    preview_mode: FirstPresentablePreviewMode
    preview_status: FirstPresentablePreviewStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    operator_facing_ready: bool
    delivery_ready: bool
    presentable_ready: bool
    truth_bound_preview: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstPresentablePreviewContract:
    """Canonical first presentable preview contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstPresentablePreviewEntry, ...]


def build_visual_first_presentable_preview_contract(
) -> VisualFirstPresentablePreviewContract:
    """Build canonical first presentable preview contract."""
    delivery_contract = build_visual_preview_delivery_readiness_contract()
    delivery_entry = delivery_contract.entries[0]

    entries = (
        VisualFirstPresentablePreviewEntry(
            preview_id="visual_first_presentable_preview_001",
            delivery_readiness_id=delivery_entry.readiness_id,
            preview_mode="first_presentable_preview",
            preview_status="presentable_preview_ready",
            renderer_surface_id=delivery_entry.renderer_surface_id,
            theme_id=delivery_entry.theme_id,
            screen_id=delivery_entry.screen_id,
            preview_artifact_id=delivery_entry.preview_artifact_id,
            operator_facing_ready=delivery_entry.operator_facing_ready,
            delivery_ready=delivery_entry.delivery_ready,
            presentable_ready=True,
            truth_bound_preview=True,
            read_only=True,
            description=(
                "Canonical first presentable preview entry after "
                "truth-preserving preview delivery readiness."
            ),
        ),
    )

    return VisualFirstPresentablePreviewContract(
        contract_id="visual_first_presentable_preview_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.preview_status == "presentable_preview_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )
