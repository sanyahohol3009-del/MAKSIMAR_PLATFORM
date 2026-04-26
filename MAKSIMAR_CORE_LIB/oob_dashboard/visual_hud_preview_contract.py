from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_snapshot_contract import (
    build_visual_hud_snapshot_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualHudPreviewContract:
    preview_id: str
    snapshot_id: str
    preview_ready: bool
    renderer_preview_enabled: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.preview_id, "preview_id")
        _require_non_empty(self.snapshot_id, "snapshot_id")
        _require_non_empty(self.description, "description")

        if not self.preview_ready:
            raise ValueError(
                "preview_ready must remain true for canonical visual HUD preview contract."
            )
        if not self.renderer_preview_enabled:
            raise ValueError(
                "renderer_preview_enabled must remain true for canonical visual HUD preview contract."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual HUD preview contract."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual HUD preview contract."
            )


def build_visual_hud_preview_contract() -> VisualHudPreviewContract:
    snapshot_contract = build_visual_hud_snapshot_contract()

    return VisualHudPreviewContract(
        preview_id="visual_hud_preview_contract_001",
        snapshot_id=snapshot_contract.snapshot_id,
        preview_ready=True,
        renderer_preview_enabled=True,
        operator_visible=True,
        truth_bound=True,
        description="Canonical visual HUD preview contract.",
    )
