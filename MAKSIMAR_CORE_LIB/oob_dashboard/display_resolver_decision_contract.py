from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_registry_contract import (
    build_display_assignment_registry_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_placement_routing_contract import (
    build_display_placement_routing_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_restore_continuity_contract import (
    build_display_restore_continuity_contract,
)


ResolverDecisionState = Literal[
    "resolver_decision_ready",
]

ResolverDecisionClass = Literal[
    "pinned_display_resolution",
    "replaceable_display_resolution",
]

ALL_RESOLVER_DECISION_STATES: tuple[ResolverDecisionState, ...] = (
    "resolver_decision_ready",
)

ALL_RESOLVER_DECISION_CLASSES: tuple[ResolverDecisionClass, ...] = (
    "pinned_display_resolution",
    "replaceable_display_resolution",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class DisplayResolverDecisionEntry:
    """Canonical display resolver decision entry."""

    resolver_decision_id: str
    display_target_id: str
    resolver_decision_state: ResolverDecisionState
    resolver_decision_class: ResolverDecisionClass
    selected_assignment_id: str
    continuity_id: str
    routed_candidate_display_target_id: str | None
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical display resolver decision entry."""
        _require_non_empty(self.resolver_decision_id, "resolver_decision_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.selected_assignment_id, "selected_assignment_id")
        _require_non_empty(self.continuity_id, "continuity_id")
        _require_non_empty(self.description, "description")

        if self.resolver_decision_state not in ALL_RESOLVER_DECISION_STATES:
            raise ValueError(
                "resolver_decision_state must be one of "
                f"{ALL_RESOLVER_DECISION_STATES}, got {self.resolver_decision_state!r}."
            )

        if self.resolver_decision_class not in ALL_RESOLVER_DECISION_CLASSES:
            raise ValueError(
                "resolver_decision_class must be one of "
                f"{ALL_RESOLVER_DECISION_CLASSES}, got {self.resolver_decision_class!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical resolver decision entries."
            )

        if (
            self.resolver_decision_class == "pinned_display_resolution"
            and self.routed_candidate_display_target_id is not None
        ):
            raise ValueError(
                "pinned_display_resolution entries must not expose routed_candidate_display_target_id."
            )

        if (
            self.resolver_decision_class == "replaceable_display_resolution"
            and self.routed_candidate_display_target_id is None
        ):
            raise ValueError(
                "replaceable_display_resolution entries must expose routed_candidate_display_target_id."
            )


@dataclass(frozen=True, slots=True)
class DisplayResolverDecisionContract:
    """Canonical display resolver decision contract."""

    contract_id: str
    total_entries: int
    pinned_resolution_entries: int
    replaceable_resolution_entries: int
    operator_visible_entries: int
    entries: tuple[DisplayResolverDecisionEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical display resolver decision contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.pinned_resolution_entries != sum(
            1
            for entry in self.entries
            if entry.resolver_decision_class == "pinned_display_resolution"
        ):
            raise ValueError(
                "pinned_resolution_entries must match pinned_display_resolution count."
            )

        if self.replaceable_resolution_entries != sum(
            1
            for entry in self.entries
            if entry.resolver_decision_class == "replaceable_display_resolution"
        ):
            raise ValueError(
                "replaceable_resolution_entries must match replaceable_display_resolution count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_display_resolver_decision_contract() -> DisplayResolverDecisionContract:
    """Build canonical display resolver decision contract."""
    assignment_contract = build_display_assignment_registry_contract()
    placement_routing_contract = build_display_placement_routing_contract()
    continuity_contract = build_display_restore_continuity_contract()

    assignments_by_display = {
        entry.display_target_id: entry.assignment_id
        for entry in assignment_contract.entries
        if entry.display_target_id in {
            "display_primary_operator",
            "display_secondary_diagnostics",
        }
    }

    continuity_by_display = {
        entry.display_target_id: entry.continuity_id
        for entry in continuity_contract.entries
        if entry.display_target_id in {
            "display_primary_operator",
            "display_secondary_diagnostics",
        }
    }

    routing_by_display = {
        entry.display_target_id: entry
        for entry in placement_routing_contract.entries
    }

    entries = (
        DisplayResolverDecisionEntry(
            resolver_decision_id="display_resolver_decision_001",
            display_target_id="display_primary_operator",
            resolver_decision_state="resolver_decision_ready",
            resolver_decision_class="pinned_display_resolution",
            selected_assignment_id=assignments_by_display["display_primary_operator"],
            continuity_id=continuity_by_display["display_primary_operator"],
            routed_candidate_display_target_id=None,
            operator_visible=True,
            description=(
                "Canonical resolver decision for pinned primary operator display."
            ),
        ),
        DisplayResolverDecisionEntry(
            resolver_decision_id="display_resolver_decision_002",
            display_target_id="display_secondary_diagnostics",
            resolver_decision_state="resolver_decision_ready",
            resolver_decision_class="replaceable_display_resolution",
            selected_assignment_id=routing_by_display[
                "display_secondary_diagnostics"
            ].incumbent_assignment_id,
            continuity_id=continuity_by_display["display_secondary_diagnostics"],
            routed_candidate_display_target_id=routing_by_display[
                "display_secondary_diagnostics"
            ].candidate_display_target_id,
            operator_visible=True,
            description=(
                "Canonical resolver decision for replaceable secondary diagnostics display."
            ),
        ),
    )

    return DisplayResolverDecisionContract(
        contract_id="display_resolver_decision_contract_001",
        total_entries=len(entries),
        pinned_resolution_entries=sum(
            1
            for entry in entries
            if entry.resolver_decision_class == "pinned_display_resolution"
        ),
        replaceable_resolution_entries=sum(
            1
            for entry in entries
            if entry.resolver_decision_class == "replaceable_display_resolution"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
