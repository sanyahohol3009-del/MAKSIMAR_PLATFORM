from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_to_visual_mapping_contract import (
    build_panel_to_visual_mapping_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualTopologyOverlayEntry:
    topology_overlay_entry_id: str
    panel_id: str
    topology_overlay_enabled: bool
    topology_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.topology_overlay_entry_id, "topology_overlay_entry_id")
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.description, "description")

        if not self.topology_overlay_enabled:
            raise ValueError(
                "topology_overlay_enabled must remain true for canonical visual topology overlay entries."
            )
        if not self.topology_ready:
            raise ValueError(
                "topology_ready must remain true for canonical visual topology overlay entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual topology overlay entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual topology overlay entries."
            )


@dataclass(frozen=True, slots=True)
class VisualTopologyOverlayContract:
    contract_id: str
    total_entries: int
    topology_ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[VisualTopologyOverlayEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.topology_ready_entries != sum(
            1 for entry in self.entries if entry.topology_ready
        ):
            raise ValueError("topology_ready_entries must match topology_ready count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError("operator_visible_entries must match operator_visible count.")
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_visual_topology_overlay_contract() -> VisualTopologyOverlayContract:
    mapping_contract = build_panel_to_visual_mapping_contract()

    entries = tuple(
        VisualTopologyOverlayEntry(
            topology_overlay_entry_id=f"visual_topology_overlay_{index:03d}",
            panel_id=entry.panel_id,
            topology_overlay_enabled=True,
            topology_ready=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical visual topology overlay entry for {entry.panel_id}.",
        )
        for index, entry in enumerate(mapping_contract.entries, start=1)
        if entry.topology_overlay_enabled
    )

    return VisualTopologyOverlayContract(
        contract_id="visual_topology_overlay_contract_001",
        total_entries=len(entries),
        topology_ready_entries=sum(1 for entry in entries if entry.topology_ready),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
