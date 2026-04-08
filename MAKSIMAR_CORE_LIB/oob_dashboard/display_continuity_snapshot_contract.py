from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_registry_contract import (
    build_display_assignment_registry_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.display_resolver_decision_contract import (
    build_display_resolver_decision_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.monitor_inventory_contract import (
    build_monitor_inventory_contract,
)


ContinuitySnapshotState = Literal[
    "snapshot_ready",
]

ContinuitySnapshotClass = Literal[
    "primary_snapshot",
    "secondary_snapshot",
    "tertiary_snapshot",
]

ALL_CONTINUITY_SNAPSHOT_STATES: tuple[ContinuitySnapshotState, ...] = (
    "snapshot_ready",
)

ALL_CONTINUITY_SNAPSHOT_CLASSES: tuple[ContinuitySnapshotClass, ...] = (
    "primary_snapshot",
    "secondary_snapshot",
    "tertiary_snapshot",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class DisplayContinuitySnapshotEntry:
    """Canonical display continuity snapshot entry."""

    snapshot_id: str
    display_target_id: str
    snapshot_state: ContinuitySnapshotState
    snapshot_class: ContinuitySnapshotClass
    active_assignments: int
    selected_assignment_present: bool
    shared_surface: bool
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical display continuity snapshot entry."""
        _require_non_empty(self.snapshot_id, "snapshot_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.description, "description")

        if self.snapshot_state not in ALL_CONTINUITY_SNAPSHOT_STATES:
            raise ValueError(
                "snapshot_state must be one of "
                f"{ALL_CONTINUITY_SNAPSHOT_STATES}, got {self.snapshot_state!r}."
            )

        if self.snapshot_class not in ALL_CONTINUITY_SNAPSHOT_CLASSES:
            raise ValueError(
                "snapshot_class must be one of "
                f"{ALL_CONTINUITY_SNAPSHOT_CLASSES}, got {self.snapshot_class!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical continuity snapshot entries."
            )

        if self.active_assignments < 1:
            raise ValueError(
                "active_assignments must be at least 1 for canonical continuity snapshots."
            )

        if not self.selected_assignment_present:
            raise ValueError(
                "selected_assignment_present must remain true for canonical continuity snapshots."
            )


@dataclass(frozen=True, slots=True)
class DisplayContinuitySnapshotContract:
    """Canonical display continuity snapshot contract."""

    contract_id: str
    total_entries: int
    shared_surface_entries: int
    operator_visible_entries: int
    entries: tuple[DisplayContinuitySnapshotEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical display continuity snapshot contract."""
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

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_display_continuity_snapshot_contract() -> DisplayContinuitySnapshotContract:
    """Build canonical display continuity snapshot contract."""
    assignment_contract = build_display_assignment_registry_contract()
    monitor_inventory_contract = build_monitor_inventory_contract()
    resolver_contract = build_display_resolver_decision_contract()

    active_assignments_by_display: dict[str, int] = {}
    for entry in assignment_contract.entries:
        active_assignments_by_display[entry.display_target_id] = (
            active_assignments_by_display.get(entry.display_target_id, 0) + 1
        )

    shared_surface_by_display = {
        entry.display_target_id: entry.shared_surface
        for entry in monitor_inventory_contract.entries
    }

    resolved_display_ids = {
        entry.display_target_id for entry in resolver_contract.entries
    }

    snapshot_class_map = {
        "display_primary_operator": "primary_snapshot",
        "display_secondary_diagnostics": "secondary_snapshot",
        "display_tertiary_expansion": "tertiary_snapshot",
    }

    entries = tuple(
        DisplayContinuitySnapshotEntry(
            snapshot_id=f"display_continuity_snapshot_{index:03d}",
            display_target_id=display_target_id,
            snapshot_state="snapshot_ready",
            snapshot_class=snapshot_class_map[display_target_id],
            active_assignments=active_assignments_by_display[display_target_id],
            selected_assignment_present=(
                display_target_id in resolved_display_ids
                or display_target_id == "display_tertiary_expansion"
            ),
            shared_surface=shared_surface_by_display[display_target_id],
            operator_visible=True,
            description=(
                f"Canonical continuity snapshot entry for {display_target_id}."
            ),
        )
        for index, display_target_id in enumerate(
            (
                "display_primary_operator",
                "display_secondary_diagnostics",
                "display_tertiary_expansion",
            ),
            start=1,
        )
    )

    return DisplayContinuitySnapshotContract(
        contract_id="display_continuity_snapshot_contract_001",
        total_entries=len(entries),
        shared_surface_entries=sum(1 for entry in entries if entry.shared_surface),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
