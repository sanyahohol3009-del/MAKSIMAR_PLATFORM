from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_continuity_snapshot_contract import (
    build_display_continuity_snapshot_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_resolver_decision_contract import (
    build_display_resolver_decision_contract,
)


ProjectionState = Literal[
    "projection_ready",
]
ProjectionClass = Literal[
    "foundation_primary_projection",
    "foundation_secondary_projection",
    "operator_interaction_projection",
]

ALL_PROJECTION_STATES: tuple[ProjectionState, ...] = (
    "projection_ready",
)
ALL_PROJECTION_CLASSES: tuple[ProjectionClass, ...] = (
    "foundation_primary_projection",
    "foundation_secondary_projection",
    "operator_interaction_projection",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class DisplayVisualProjectionEntry:
    """Canonical display visual projection entry."""

    projection_id: str
    display_target_id: str
    projection_state: ProjectionState
    projection_class: ProjectionClass
    selected_assignment_present: bool
    shared_surface: bool
    projection_ready: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical display visual projection entry."""
        _require_non_empty(self.projection_id, "projection_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.description, "description")

        if self.projection_state not in ALL_PROJECTION_STATES:
            raise ValueError(
                "projection_state must be one of "
                f"{ALL_PROJECTION_STATES}, got {self.projection_state!r}."
            )

        if self.projection_class not in ALL_PROJECTION_CLASSES:
            raise ValueError(
                "projection_class must be one of "
                f"{ALL_PROJECTION_CLASSES}, got {self.projection_class!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical visual projection entries."
            )

        if not self.selected_assignment_present:
            raise ValueError(
                "selected_assignment_present must remain true for canonical visual projection entries."
            )

        if not self.projection_ready:
            raise ValueError(
                "projection_ready must remain true for canonical visual projection entries."
            )


@dataclass(frozen=True, slots=True)
class DisplayVisualProjectionContract:
    """Canonical display visual projection contract."""

    contract_id: str
    total_entries: int
    shared_surface_entries: int
    ready_entries: int
    operator_visible_entries: int
    entries: tuple[DisplayVisualProjectionEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical display visual projection contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.shared_surface_entries != sum(
            1 for entry in self.entries if entry.shared_surface
        ):
            raise ValueError(
                "shared_surface_entries must match shared_surface count."
            )

        if self.ready_entries != sum(
            1 for entry in self.entries if entry.projection_ready
        ):
            raise ValueError("ready_entries must match projection_ready count.")

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_display_visual_projection_contract() -> DisplayVisualProjectionContract:
    """Build canonical display visual projection contract."""
    continuity_snapshot_contract = build_display_continuity_snapshot_contract()
    resolver_decision_contract = build_display_resolver_decision_contract()

    resolved_display_ids = {
        entry.display_target_id for entry in resolver_decision_contract.entries
    }

    projection_class_map: dict[str, ProjectionClass] = {
        "display_foundation_primary": "foundation_primary_projection",
        "display_foundation_secondary": "foundation_secondary_projection",
        "display_operator_interaction": "operator_interaction_projection",
    }

    entries = tuple(
        DisplayVisualProjectionEntry(
            projection_id=f"display_visual_projection_{index:03d}",
            display_target_id=entry.display_target_id,
            projection_state="projection_ready",
            projection_class=projection_class_map[entry.display_target_id],
            selected_assignment_present=entry.display_target_id in resolved_display_ids
            or entry.display_target_id == "display_operator_interaction",
            shared_surface=entry.shared_surface,
            projection_ready=True,
            operator_visible=True,
            description=(
                f"Canonical display visual projection entry for {entry.display_target_id}."
            ),
        )
        for index, entry in enumerate(continuity_snapshot_contract.entries, start=1)
    )

    return DisplayVisualProjectionContract(
        contract_id="display_visual_projection_contract_001",
        total_entries=len(entries),
        shared_surface_entries=sum(1 for entry in entries if entry.shared_surface),
        ready_entries=sum(1 for entry in entries if entry.projection_ready),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
