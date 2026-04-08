from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_registry_contract import (
    build_display_assignment_registry_contract,
)


DisplayOccupancyState = Literal[
    "occupied_pinned",
    "occupied_replaceable",
]

DisplayOccupancyClass = Literal[
    "primary_operator_display",
    "secondary_diagnostics_display",
    "tertiary_expansion_display",
]

ALL_DISPLAY_OCCUPANCY_STATES: tuple[DisplayOccupancyState, ...] = (
    "occupied_pinned",
    "occupied_replaceable",
)

ALL_DISPLAY_OCCUPANCY_CLASSES: tuple[DisplayOccupancyClass, ...] = (
    "primary_operator_display",
    "secondary_diagnostics_display",
    "tertiary_expansion_display",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class DisplayOccupancyEntry:
    """Canonical display occupancy entry."""

    display_target_id: str
    occupancy_state: DisplayOccupancyState
    occupancy_class: DisplayOccupancyClass
    total_assignments: int
    replaceable_assignments: int
    pinned_assignments: int
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical display occupancy entry."""
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.description, "description")

        if self.occupancy_state not in ALL_DISPLAY_OCCUPANCY_STATES:
            raise ValueError(
                "occupancy_state must be one of "
                f"{ALL_DISPLAY_OCCUPANCY_STATES}, got {self.occupancy_state!r}."
            )

        if self.occupancy_class not in ALL_DISPLAY_OCCUPANCY_CLASSES:
            raise ValueError(
                "occupancy_class must be one of "
                f"{ALL_DISPLAY_OCCUPANCY_CLASSES}, got {self.occupancy_class!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical display occupancy entries."
            )

        if self.total_assignments != (
            self.replaceable_assignments + self.pinned_assignments
        ):
            raise ValueError(
                "total_assignments must equal replaceable_assignments + pinned_assignments."
            )

        if self.occupancy_state == "occupied_pinned" and self.pinned_assignments < 1:
            raise ValueError(
                "occupied_pinned entries must contain at least one pinned assignment."
            )

        if (
            self.occupancy_state == "occupied_replaceable"
            and self.replaceable_assignments < 1
        ):
            raise ValueError(
                "occupied_replaceable entries must contain at least one replaceable assignment."
            )


@dataclass(frozen=True, slots=True)
class DisplayOccupancyContract:
    """Canonical display occupancy contract."""

    contract_id: str
    total_entries: int
    pinned_entries: int
    replaceable_entries: int
    operator_visible_entries: int
    entries: tuple[DisplayOccupancyEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical display occupancy contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.pinned_entries != sum(
            1 for entry in self.entries if entry.occupancy_state == "occupied_pinned"
        ):
            raise ValueError("pinned_entries must match occupied_pinned count.")

        if self.replaceable_entries != sum(
            1
            for entry in self.entries
            if entry.occupancy_state == "occupied_replaceable"
        ):
            raise ValueError(
                "replaceable_entries must match occupied_replaceable count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_display_occupancy_contract() -> DisplayOccupancyContract:
    """Build canonical display occupancy contract."""
    registry_contract = build_display_assignment_registry_contract()

    assignments_by_display: dict[str, list[bool]] = {}
    for entry in registry_contract.entries:
        assignments_by_display.setdefault(entry.display_target_id, []).append(
            entry.replaceable
        )

    class_map = {
        "display_primary_operator": "primary_operator_display",
        "display_secondary_diagnostics": "secondary_diagnostics_display",
        "display_tertiary_expansion": "tertiary_expansion_display",
    }

    entries = tuple(
        DisplayOccupancyEntry(
            display_target_id=display_target_id,
            occupancy_state=(
                "occupied_replaceable"
                if all(replaceable_flags)
                else "occupied_pinned"
            ),
            occupancy_class=class_map[display_target_id],
            total_assignments=len(replaceable_flags),
            replaceable_assignments=sum(1 for flag in replaceable_flags if flag),
            pinned_assignments=sum(1 for flag in replaceable_flags if not flag),
            operator_visible=True,
            description=(
                f"Canonical display occupancy entry for {display_target_id}."
            ),
        )
        for display_target_id, replaceable_flags in assignments_by_display.items()
    )

    return DisplayOccupancyContract(
        contract_id="display_occupancy_contract_001",
        total_entries=len(entries),
        pinned_entries=sum(
            1 for entry in entries if entry.occupancy_state == "occupied_pinned"
        ),
        replaceable_entries=sum(
            1
            for entry in entries
            if entry.occupancy_state == "occupied_replaceable"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
