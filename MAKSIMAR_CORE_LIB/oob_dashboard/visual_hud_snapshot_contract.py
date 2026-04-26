from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_composition_contract import (
    build_visual_hud_composition_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualHudSnapshotContract:
    snapshot_id: str
    composition_id: str
    snapshot_ready: bool
    preview_safe: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.snapshot_id, "snapshot_id")
        _require_non_empty(self.composition_id, "composition_id")
        _require_non_empty(self.description, "description")

        if not self.snapshot_ready:
            raise ValueError(
                "snapshot_ready must remain true for canonical visual HUD snapshot contract."
            )
        if not self.preview_safe:
            raise ValueError(
                "preview_safe must remain true for canonical visual HUD snapshot contract."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual HUD snapshot contract."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual HUD snapshot contract."
            )


def build_visual_hud_snapshot_contract() -> VisualHudSnapshotContract:
    composition_contract = build_visual_hud_composition_contract()

    return VisualHudSnapshotContract(
        snapshot_id="visual_hud_snapshot_contract_001",
        composition_id=composition_contract.composition_id,
        snapshot_ready=True,
        preview_safe=True,
        operator_visible=True,
        truth_bound=True,
        description="Canonical visual HUD snapshot contract.",
    )
