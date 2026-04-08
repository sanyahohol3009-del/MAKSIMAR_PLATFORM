from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_registry_contract import (
    build_display_assignment_registry_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_conflict_resolution_contract import (
    build_display_conflict_resolution_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.free_display_selection_contract import (
    build_free_display_selection_contract,
)


PlacementRoutingState = Literal[
    "placement_route_resolved",
]

PlacementRoutingClass = Literal[
    "pinned_route",
    "replaceable_route",
]

ALL_PLACEMENT_ROUTING_STATES: tuple[PlacementRoutingState, ...] = (
    "placement_route_resolved",
)

ALL_PLACEMENT_ROUTING_CLASSES: tuple[PlacementRoutingClass, ...] = (
    "pinned_route",
    "replaceable_route",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class DisplayPlacementRoutingEntry:
    """Canonical display placement routing entry."""

    routing_id: str
    display_target_id: str
    routing_state: PlacementRoutingState
    routing_class: PlacementRoutingClass
    incumbent_assignment_id: str
    candidate_display_target_id: str | None
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical display placement routing entry."""
        _require_non_empty(self.routing_id, "routing_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.incumbent_assignment_id, "incumbent_assignment_id")
        _require_non_empty(self.description, "description")

        if self.routing_state not in ALL_PLACEMENT_ROUTING_STATES:
            raise ValueError(
                "routing_state must be one of "
                f"{ALL_PLACEMENT_ROUTING_STATES}, got {self.routing_state!r}."
            )

        if self.routing_class not in ALL_PLACEMENT_ROUTING_CLASSES:
            raise ValueError(
                "routing_class must be one of "
                f"{ALL_PLACEMENT_ROUTING_CLASSES}, got {self.routing_class!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical placement routing entries."
            )

        if self.routing_class == "pinned_route" and self.candidate_display_target_id is not None:
            raise ValueError(
                "pinned_route entries must not expose candidate_display_target_id."
            )

        if self.routing_class == "replaceable_route" and self.candidate_display_target_id is None:
            raise ValueError(
                "replaceable_route entries must expose candidate_display_target_id."
            )


@dataclass(frozen=True, slots=True)
class DisplayPlacementRoutingContract:
    """Canonical display placement routing contract."""

    contract_id: str
    total_entries: int
    pinned_route_entries: int
    replaceable_route_entries: int
    operator_visible_entries: int
    entries: tuple[DisplayPlacementRoutingEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical display placement routing contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.pinned_route_entries != sum(
            1 for entry in self.entries if entry.routing_class == "pinned_route"
        ):
            raise ValueError(
                "pinned_route_entries must match pinned_route count."
            )

        if self.replaceable_route_entries != sum(
            1 for entry in self.entries if entry.routing_class == "replaceable_route"
        ):
            raise ValueError(
                "replaceable_route_entries must match replaceable_route count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_display_placement_routing_contract() -> DisplayPlacementRoutingContract:
    """Build canonical display placement routing contract."""
    assignment_registry = build_display_assignment_registry_contract()
    conflict_contract = build_display_conflict_resolution_contract()
    free_selection_contract = build_free_display_selection_contract()

    assignments_by_display = {
        entry.display_target_id: entry.assignment_id
        for entry in assignment_registry.entries
    }

    selection_entry = free_selection_contract.entries[0]
    conflict_map = {entry.display_target_id: entry for entry in conflict_contract.entries}

    entries = (
        DisplayPlacementRoutingEntry(
            routing_id="display_placement_route_001",
            display_target_id="display_primary_operator",
            routing_state="placement_route_resolved",
            routing_class="pinned_route",
            incumbent_assignment_id=assignments_by_display["display_primary_operator"],
            candidate_display_target_id=None,
            operator_visible=True,
            description="Canonical placement route retaining pinned primary operator display.",
        ),
        DisplayPlacementRoutingEntry(
            routing_id="display_placement_route_002",
            display_target_id="display_secondary_diagnostics",
            routing_state="placement_route_resolved",
            routing_class="replaceable_route",
            incumbent_assignment_id=conflict_map["display_secondary_diagnostics"].incumbent_assignment_id,
            candidate_display_target_id=selection_entry.candidate_display_target_id,
            operator_visible=True,
            description="Canonical placement route using replaceable diagnostics display candidate.",
        ),
    )

    return DisplayPlacementRoutingContract(
        contract_id="display_placement_routing_contract_001",
        total_entries=len(entries),
        pinned_route_entries=sum(
            1 for entry in entries if entry.routing_class == "pinned_route"
        ),
        replaceable_route_entries=sum(
            1 for entry in entries if entry.routing_class == "replaceable_route"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
