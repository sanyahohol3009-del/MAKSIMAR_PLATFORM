from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_to_visual_mapping_contract import (
    build_panel_to_visual_mapping_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualRenderSurfaceEntry:
    render_surface_id: str
    panel_id: str
    preferred_zone: str
    visual_card_type: str
    render_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.render_surface_id, "render_surface_id")
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.preferred_zone, "preferred_zone")
        _require_non_empty(self.visual_card_type, "visual_card_type")
        _require_non_empty(self.description, "description")

        if not self.render_ready:
            raise ValueError(
                "render_ready must remain true for canonical visual render surface entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual render surface entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual render surface entries."
            )


@dataclass(frozen=True, slots=True)
class VisualRenderSurfaceContract:
    contract_id: str
    total_entries: int
    render_ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[VisualRenderSurfaceEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.render_ready_entries != sum(
            1 for entry in self.entries if entry.render_ready
        ):
            raise ValueError("render_ready_entries must match render_ready count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError("operator_visible_entries must match operator_visible count.")
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_visual_render_surface_contract() -> VisualRenderSurfaceContract:
    mapping_contract = build_panel_to_visual_mapping_contract()

    entries = tuple(
        VisualRenderSurfaceEntry(
            render_surface_id=f"visual_render_surface_{index:03d}",
            panel_id=entry.panel_id,
            preferred_zone=entry.preferred_zone,
            visual_card_type=entry.visual_card_type,
            render_ready=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical visual render surface entry for {entry.panel_id}.",
        )
        for index, entry in enumerate(mapping_contract.entries, start=1)
    )

    return VisualRenderSurfaceContract(
        contract_id="visual_render_surface_contract_001",
        total_entries=len(entries),
        render_ready_entries=sum(1 for entry in entries if entry.render_ready),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
