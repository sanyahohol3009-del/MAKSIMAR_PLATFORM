from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.interaction_exposure_contract import (
    build_interaction_exposure_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class InteractionObservabilityEntry:
    observability_entry_id: str
    exposure_entry_id: str
    observable: bool
    incident_trackable: bool
    direct_execution_allowed: bool
    operator_visible: bool
    truth_bound: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.observability_entry_id, "observability_entry_id")
        _require_non_empty(self.exposure_entry_id, "exposure_entry_id")
        _require_non_empty(self.description, "description")

        if not self.observable:
            raise ValueError(
                "observable must remain true for canonical interaction observability entries."
            )
        if not self.incident_trackable:
            raise ValueError(
                "incident_trackable must remain true for canonical interaction observability entries."
            )
        if self.direct_execution_allowed:
            raise ValueError(
                "direct_execution_allowed must remain false for canonical interaction observability entries."
            )
        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical interaction observability entries."
            )
        if not self.truth_bound:
            raise ValueError(
                "truth_bound must remain true for canonical interaction observability entries."
            )


@dataclass(frozen=True, slots=True)
class InteractionObservabilityContract:
    contract_id: str
    total_entries: int
    observable_entries: int
    incident_trackable_entries: int
    guarded_entries: int
    operator_visible_entries: int
    truth_bound_entries: int
    entries: tuple[InteractionObservabilityEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")
        if self.observable_entries != sum(
            1 for entry in self.entries if entry.observable
        ):
            raise ValueError("observable_entries must match observable count.")
        if self.incident_trackable_entries != sum(
            1 for entry in self.entries if entry.incident_trackable
        ):
            raise ValueError(
                "incident_trackable_entries must match incident_trackable count."
            )
        if self.guarded_entries != sum(
            1 for entry in self.entries if entry.direct_execution_allowed is False
        ):
            raise ValueError("guarded_entries must match guarded observability count.")
        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError("operator_visible_entries must match operator_visible count.")
        if self.truth_bound_entries != sum(
            1 for entry in self.entries if entry.truth_bound
        ):
            raise ValueError("truth_bound_entries must match truth_bound count.")


def build_interaction_observability_contract() -> InteractionObservabilityContract:
    exposure_contract = build_interaction_exposure_contract()

    entries = tuple(
        InteractionObservabilityEntry(
            observability_entry_id=f"interaction_observability_{index:03d}",
            exposure_entry_id=entry.exposure_entry_id,
            observable=True,
            incident_trackable=True,
            direct_execution_allowed=False,
            operator_visible=True,
            truth_bound=True,
            description=f"Canonical interaction observability entry for {entry.exposure_entry_id}.",
        )
        for index, entry in enumerate(exposure_contract.entries, start=1)
    )

    return InteractionObservabilityContract(
        contract_id="interaction_observability_contract_001",
        total_entries=len(entries),
        observable_entries=sum(1 for entry in entries if entry.observable),
        incident_trackable_entries=sum(1 for entry in entries if entry.incident_trackable),
        guarded_entries=sum(1 for entry in entries if entry.direct_execution_allowed is False),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        truth_bound_entries=sum(1 for entry in entries if entry.truth_bound),
        entries=entries,
    )
