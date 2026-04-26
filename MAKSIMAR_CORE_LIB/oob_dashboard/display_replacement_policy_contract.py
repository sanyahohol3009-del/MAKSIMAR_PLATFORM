from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_registry_contract import (
    build_display_assignment_registry_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_occupancy_contract import (
    build_display_occupancy_contract,
)


ReplacementDecision = Literal[
    "not_replaceable",
    "replaceable_without_disruption",
]
ReplacementClass = Literal[
    "foundation_primary_pinned_surface",
    "foundation_secondary_replaceable_surface",
    "operator_interaction_replaceable_surface",
]

ALL_REPLACEMENT_DECISIONS: tuple[ReplacementDecision, ...] = (
    "not_replaceable",
    "replaceable_without_disruption",
)
ALL_REPLACEMENT_CLASSES: tuple[ReplacementClass, ...] = (
    "foundation_primary_pinned_surface",
    "foundation_secondary_replaceable_surface",
    "operator_interaction_replaceable_surface",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class DisplayReplacementPolicyEntry:
    """Canonical display replacement policy entry."""

    display_target_id: str
    replacement_decision: ReplacementDecision
    replacement_class: ReplacementClass
    active_assignments: int
    replaceable_assignments: int
    pinned_assignments: int
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical display replacement policy entry."""
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.description, "description")

        if self.replacement_decision not in ALL_REPLACEMENT_DECISIONS:
            raise ValueError("invalid replacement_decision")

        if self.replacement_class not in ALL_REPLACEMENT_CLASSES:
            raise ValueError("invalid replacement_class")

        if not self.operator_visible:
            raise ValueError("operator_visible must remain true")

        if self.active_assignments != (
            self.replaceable_assignments + self.pinned_assignments
        ):
            raise ValueError(
                "active_assignments must equal replaceable_assignments + pinned_assignments."
            )

        if (
            self.replacement_decision == "not_replaceable"
            and self.pinned_assignments < 1
        ):
            raise ValueError("not_replaceable must have pinned assignments")

        if (
            self.replacement_decision == "replaceable_without_disruption"
            and self.replaceable_assignments < 1
        ):
            raise ValueError("replaceable entries must have replaceable assignments")


@dataclass(frozen=True, slots=True)
class DisplayReplacementPolicyContract:
    """Canonical display replacement policy contract."""

    contract_id: str
    total_entries: int
    not_replaceable_entries: int
    replaceable_entries: int
    operator_visible_entries: int
    entries: tuple[DisplayReplacementPolicyEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical display replacement policy contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries mismatch")

        if self.not_replaceable_entries != sum(
            1 for e in self.entries if e.replacement_decision == "not_replaceable"
        ):
            raise ValueError("not_replaceable_entries mismatch")

        if self.replaceable_entries != sum(
            1
            for e in self.entries
            if e.replacement_decision == "replaceable_without_disruption"
        ):
            raise ValueError("replaceable_entries mismatch")

        if self.operator_visible_entries != sum(
            1 for e in self.entries if e.operator_visible
        ):
            raise ValueError("operator_visible_entries mismatch")


def build_display_replacement_policy_contract() -> DisplayReplacementPolicyContract:
    """Build canonical display replacement policy contract."""
    assignment_registry = build_display_assignment_registry_contract()
    occupancy_contract = build_display_occupancy_contract()

    counts: dict[str, dict[str, int]] = {}
    for entry in assignment_registry.entries:
        stats = counts.setdefault(
            entry.display_target_id,
            {"active": 0, "replaceable": 0, "pinned": 0},
        )
        stats["active"] += 1
        if entry.replaceable:
            stats["replaceable"] += 1
        else:
            stats["pinned"] += 1

    replacement_class_map: dict[str, ReplacementClass] = {
        "display_foundation_primary": "foundation_primary_pinned_surface",
        "display_foundation_secondary": "foundation_secondary_replaceable_surface",
        "display_operator_interaction": "operator_interaction_replaceable_surface",
    }

    occupancy_map = {e.display_target_id: e for e in occupancy_contract.entries}

    entries = tuple(
        DisplayReplacementPolicyEntry(
            display_target_id=display_id,
            replacement_decision=(
                "not_replaceable"
                if occupancy_map[display_id].occupancy_state == "occupied_pinned"
                else "replaceable_without_disruption"
            ),
            replacement_class=replacement_class_map[display_id],
            active_assignments=stats["active"],
            replaceable_assignments=stats["replaceable"],
            pinned_assignments=stats["pinned"],
            operator_visible=True,
            description=f"Replacement policy for {display_id}",
        )
        for display_id, stats in counts.items()
    )

    return DisplayReplacementPolicyContract(
        contract_id="display_replacement_policy_contract_001",
        total_entries=len(entries),
        not_replaceable_entries=sum(
            1 for e in entries if e.replacement_decision == "not_replaceable"
        ),
        replaceable_entries=sum(
            1
            for e in entries
            if e.replacement_decision == "replaceable_without_disruption"
        ),
        operator_visible_entries=sum(1 for e in entries if e.operator_visible),
        entries=entries,
    )
