from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_capability_matrix_contract import (
    build_visual_capability_matrix_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class VisualDegradedModeCapabilityEntry:
    degraded_entry_id: str
    backend_id: str
    degraded_mode_id: str
    reduced_graph_density: bool
    reduced_chart_density: bool
    reduced_overlay_density: bool
    reduced_motion_density: bool
    readable_operator_state_preserved: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.degraded_entry_id, "degraded_entry_id")
        _require_non_empty(self.backend_id, "backend_id")
        _require_non_empty(self.degraded_mode_id, "degraded_mode_id")
        _require_non_empty(self.description, "description")

        if not any(
            (
                self.reduced_graph_density,
                self.reduced_chart_density,
                self.reduced_overlay_density,
                self.reduced_motion_density,
            )
        ):
            raise ValueError(
                "At least one reduced_* flag must remain true for canonical degraded capability entries."
            )
        if not self.readable_operator_state_preserved:
            raise ValueError(
                "readable_operator_state_preserved must remain true for canonical degraded capability entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical degraded capability entries."
            )


@dataclass(frozen=True, slots=True)
class VisualDegradedModeCapabilityContract:
    contract_id: str
    total_entries: int
    readable_operator_state_preserved_entries: int
    truth_bound_entries: int
    entries: Tuple[VisualDegradedModeCapabilityEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.readable_operator_state_preserved_entries != sum(
            1 for entry in self.entries if entry.readable_operator_state_preserved
        ):
            raise ValueError(
                "readable_operator_state_preserved_entries must match readable_operator_state_preserved count."
            )
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_visual_degraded_mode_capability_contract() -> (
    VisualDegradedModeCapabilityContract
):
    capability_contract = build_visual_capability_matrix_contract()

    entries = tuple(
        VisualDegradedModeCapabilityEntry(
            degraded_entry_id=f"visual_degraded_mode_capability_{index:03d}",
            backend_id=entry.backend_id,
            degraded_mode_id=f"{entry.backend_id}_degraded_mode",
            reduced_graph_density=entry.graph_capable,
            reduced_chart_density=entry.chart_capable,
            reduced_overlay_density=entry.overlay_capable,
            reduced_motion_density=entry.motion_capable,
            readable_operator_state_preserved=True,
            truth_bound=True,
            description=f"Canonical degraded-mode capability entry for {entry.backend_id}.",
        )
        for index, entry in enumerate(capability_contract.entries, start=1)
    )

    return VisualDegradedModeCapabilityContract(
        contract_id="visual_degraded_mode_capability_contract_001",
        total_entries=len(entries),
        readable_operator_state_preserved_entries=sum(
            1 for entry in entries if entry.readable_operator_state_preserved
        ),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
