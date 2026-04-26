from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.interaction_observability_contract import (
    build_interaction_observability_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class InteractionIncidentSurfaceEntry:
    incident_surface_entry_id: str
    observability_entry_id: str
    incident_surface_ready: bool
    visible_on_incident_surface: bool
    direct_execution_allowed: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.incident_surface_entry_id, "incident_surface_entry_id")
        _require_non_empty(self.observability_entry_id, "observability_entry_id")
        _require_non_empty(self.description, "description")

        if not self.incident_surface_ready:
            raise ValueError(
                "incident_surface_ready must remain true for canonical interaction incident surface entries."
            )
        if not self.visible_on_incident_surface:
            raise ValueError(
                "visible_on_incident_surface must remain true for canonical interaction incident surface entries."
            )
        if self.direct_execution_allowed:
            raise ValueError(
                "direct_execution_allowed must remain false for canonical interaction incident surface entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical interaction incident surface entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical interaction incident surface entries."
            )


@dataclass(frozen=True, slots=True)
class InteractionIncidentSurfaceContract:
    contract_id: str
    total_entries: int
    ready_entries: int
    visible_entries: int
    guarded_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[InteractionIncidentSurfaceEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.ready_entries != sum(
            1 for entry in self.entries if entry.incident_surface_ready
        ):
            raise ValueError("ready_entries must match incident_surface_ready count.")
        if self.visible_entries != sum(
            1 for entry in self.entries if entry.visible_on_incident_surface
        ):
            raise ValueError(
                "visible_entries must match visible_on_incident_surface count."
            )
        if self.guarded_entries != sum(
            1 for entry in self.entries if entry.direct_execution_allowed is False
        ):
            raise ValueError("guarded_entries must match guarded incident surface count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError("operator_visible_entries must match operator_visible count.")
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_interaction_incident_surface_contract() -> InteractionIncidentSurfaceContract:
    observability_contract = build_interaction_observability_contract()

    entries = tuple(
        InteractionIncidentSurfaceEntry(
            incident_surface_entry_id=f"interaction_incident_surface_{index:03d}",
            observability_entry_id=entry.observability_entry_id,
            incident_surface_ready=True,
            visible_on_incident_surface=True,
            direct_execution_allowed=False,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical interaction incident surface entry for {entry.observability_entry_id}.",
        )
        for index, entry in enumerate(observability_contract.entries, start=1)
    )

    return InteractionIncidentSurfaceContract(
        contract_id="interaction_incident_surface_contract_001",
        total_entries=len(entries),
        ready_entries=sum(1 for entry in entries if entry.incident_surface_ready),
        visible_entries=sum(1 for entry in entries if entry.visible_on_incident_surface),
        guarded_entries=sum(1 for entry in entries if entry.direct_execution_allowed is False),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
