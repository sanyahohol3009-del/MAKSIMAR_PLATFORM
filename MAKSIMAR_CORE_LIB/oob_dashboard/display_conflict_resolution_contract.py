from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_registry_contract import (
    build_display_assignment_registry_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_replacement_policy_contract import (
    build_display_replacement_policy_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.free_display_selection_contract import (
    build_free_display_selection_contract,
)


ConflictDecision = Literal[
    "retain_pinned_surface",
    "replace_replaceable_surface",
]
ConflictClass = Literal[
    "foundation_primary_conflict",
    "foundation_secondary_conflict",
]

ALL_CONFLICT_DECISIONS: tuple[ConflictDecision, ...] = (
    "retain_pinned_surface",
    "replace_replaceable_surface",
)
ALL_CONFLICT_CLASSES: tuple[ConflictClass, ...] = (
    "foundation_primary_conflict",
    "foundation_secondary_conflict",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class DisplayConflictResolutionEntry:
    """Canonical display conflict-resolution entry."""

    conflict_id: str
    display_target_id: str
    conflict_decision: ConflictDecision
    conflict_class: ConflictClass
    incumbent_assignment_id: str
    candidate_display_target_id: str | None
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical display conflict-resolution entry."""
        _require_non_empty(self.conflict_id, "conflict_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.incumbent_assignment_id, "incumbent_assignment_id")
        _require_non_empty(self.description, "description")

        if self.conflict_decision not in ALL_CONFLICT_DECISIONS:
            raise ValueError(
                "conflict_decision must be one of "
                f"{ALL_CONFLICT_DECISIONS}, got {self.conflict_decision!r}."
            )

        if self.conflict_class not in ALL_CONFLICT_CLASSES:
            raise ValueError(
                "conflict_class must be one of "
                f"{ALL_CONFLICT_CLASSES}, got {self.conflict_class!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical conflict-resolution entries."
            )

        if (
            self.conflict_decision == "retain_pinned_surface"
            and self.candidate_display_target_id is not None
        ):
            raise ValueError(
                "retain_pinned_surface entries must not expose candidate_display_target_id."
            )

        if (
            self.conflict_decision == "replace_replaceable_surface"
            and self.candidate_display_target_id is None
        ):
            raise ValueError(
                "replace_replaceable_surface entries must expose candidate_display_target_id."
            )


@dataclass(frozen=True, slots=True)
class DisplayConflictResolutionContract:
    """Canonical display conflict-resolution contract."""

    contract_id: str
    total_entries: int
    pinned_conflict_entries: int
    replaceable_conflict_entries: int
    operator_visible_entries: int
    entries: tuple[DisplayConflictResolutionEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical display conflict-resolution contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.pinned_conflict_entries != sum(
            1
            for entry in self.entries
            if entry.conflict_class == "foundation_primary_conflict"
        ):
            raise ValueError(
                "pinned_conflict_entries must match foundation_primary_conflict count."
            )

        if self.replaceable_conflict_entries != sum(
            1
            for entry in self.entries
            if entry.conflict_class == "foundation_secondary_conflict"
        ):
            raise ValueError(
                "replaceable_conflict_entries must match foundation_secondary_conflict count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_display_conflict_resolution_contract() -> DisplayConflictResolutionContract:
    """Build canonical display conflict-resolution contract."""
    assignment_registry = build_display_assignment_registry_contract()
    replacement_policy = build_display_replacement_policy_contract()
    free_display_selection = build_free_display_selection_contract()

    assignments_by_display: dict[str, list[str]] = {}
    for entry in assignment_registry.entries:
        assignments_by_display.setdefault(entry.display_target_id, []).append(
            entry.assignment_id
        )

    replacement_by_display = {
        entry.display_target_id: entry for entry in replacement_policy.entries
    }
    selection_entry = free_display_selection.entries[0]

    entries = (
        DisplayConflictResolutionEntry(
            conflict_id="display_conflict_001",
            display_target_id="display_foundation_primary",
            conflict_decision="retain_pinned_surface",
            conflict_class="foundation_primary_conflict",
            incumbent_assignment_id=assignments_by_display["display_foundation_primary"][0],
            candidate_display_target_id=None,
            operator_visible=True,
            description=(
                "Canonical conflict-resolution entry retaining the pinned foundation primary surface."
            ),
        ),
        DisplayConflictResolutionEntry(
            conflict_id="display_conflict_002",
            display_target_id="display_foundation_secondary",
            conflict_decision="replace_replaceable_surface",
            conflict_class="foundation_secondary_conflict",
            incumbent_assignment_id=assignments_by_display["display_foundation_secondary"][0],
            candidate_display_target_id=selection_entry.candidate_display_target_id,
            operator_visible=True,
            description=(
                "Canonical conflict-resolution entry allowing replacement on a replaceable foundation secondary surface."
            ),
        ),
    )

    # Touch replacement policy to ensure this layer remains aligned with it.
    _ = replacement_by_display["display_foundation_primary"]
    _ = replacement_by_display["display_foundation_secondary"]

    return DisplayConflictResolutionContract(
        contract_id="display_conflict_resolution_contract_001",
        total_entries=len(entries),
        pinned_conflict_entries=sum(
            1
            for entry in entries
            if entry.conflict_class == "foundation_primary_conflict"
        ),
        replaceable_conflict_entries=sum(
            1
            for entry in entries
            if entry.conflict_class == "foundation_secondary_conflict"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
