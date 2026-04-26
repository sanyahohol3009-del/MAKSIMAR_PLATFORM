from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_to_visual_mapping_contract import (
    build_panel_to_visual_mapping_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualSignalOverlayEntry:
    overlay_entry_id: str
    panel_id: str
    signal_overlay_enabled: bool
    overlay_ready: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.overlay_entry_id, "overlay_entry_id")
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.description, "description")

        if not self.signal_overlay_enabled:
            raise ValueError(
                "signal_overlay_enabled must remain true for canonical visual signal overlay entries."
            )
        if not self.overlay_ready:
            raise ValueError(
                "overlay_ready must remain true for canonical visual signal overlay entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual signal overlay entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical visual signal overlay entries."
            )


@dataclass(frozen=True, slots=True)
class VisualSignalOverlayContract:
    contract_id: str
    total_entries: int
    overlay_ready_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[VisualSignalOverlayEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.overlay_ready_entries != sum(
            1 for entry in self.entries if entry.overlay_ready
        ):
            raise ValueError("overlay_ready_entries must match overlay_ready count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError("operator_visible_entries must match operator_visible count.")
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_visual_signal_overlay_contract() -> VisualSignalOverlayContract:
    mapping_contract = build_panel_to_visual_mapping_contract()

    entries = tuple(
        VisualSignalOverlayEntry(
            overlay_entry_id=f"visual_signal_overlay_{index:03d}",
            panel_id=entry.panel_id,
            signal_overlay_enabled=True,
            overlay_ready=True,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical visual signal overlay entry for {entry.panel_id}.",
        )
        for index, entry in enumerate(mapping_contract.entries, start=1)
        if entry.signal_overlay_enabled
    )

    return VisualSignalOverlayContract(
        contract_id="visual_signal_overlay_contract_001",
        total_entries=len(entries),
        overlay_ready_entries=sum(1 for entry in entries if entry.overlay_ready),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
