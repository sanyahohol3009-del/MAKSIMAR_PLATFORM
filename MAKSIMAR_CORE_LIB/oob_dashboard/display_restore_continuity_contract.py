from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_assignment_restore_contract import (
    build_display_assignment_restore_contract,
)


RestoreContinuityState = Literal[
    "restore_continuity_preserved",
]

RestoreContinuityClass = Literal[
    "direct_restore_continuity",
    "shared_surface_restore_continuity",
]

ALL_RESTORE_CONTINUITY_STATES: tuple[RestoreContinuityState, ...] = (
    "restore_continuity_preserved",
)

ALL_RESTORE_CONTINUITY_CLASSES: tuple[RestoreContinuityClass, ...] = (
    "direct_restore_continuity",
    "shared_surface_restore_continuity",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class DisplayRestoreContinuityEntry:
    """Canonical display restore continuity entry."""

    continuity_id: str
    assignment_id: str
    display_target_id: str
    restore_continuity_state: RestoreContinuityState
    restore_continuity_class: RestoreContinuityClass
    workspace_id: str
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical display restore continuity entry."""
        _require_non_empty(self.continuity_id, "continuity_id")
        _require_non_empty(self.assignment_id, "assignment_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.description, "description")

        if self.restore_continuity_state not in ALL_RESTORE_CONTINUITY_STATES:
            raise ValueError(
                "restore_continuity_state must be one of "
                f"{ALL_RESTORE_CONTINUITY_STATES}, got {self.restore_continuity_state!r}."
            )

        if self.restore_continuity_class not in ALL_RESTORE_CONTINUITY_CLASSES:
            raise ValueError(
                "restore_continuity_class must be one of "
                f"{ALL_RESTORE_CONTINUITY_CLASSES}, got {self.restore_continuity_class!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical restore continuity entries."
            )


@dataclass(frozen=True, slots=True)
class DisplayRestoreContinuityContract:
    """Canonical display restore continuity contract."""

    contract_id: str
    total_entries: int
    direct_restore_entries: int
    shared_surface_restore_entries: int
    operator_visible_entries: int
    entries: tuple[DisplayRestoreContinuityEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical display restore continuity contract."""
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the contract."
            )

        if self.direct_restore_entries != sum(
            1
            for entry in self.entries
            if entry.restore_continuity_class == "direct_restore_continuity"
        ):
            raise ValueError(
                "direct_restore_entries must match direct_restore_continuity count."
            )

        if self.shared_surface_restore_entries != sum(
            1
            for entry in self.entries
            if entry.restore_continuity_class == "shared_surface_restore_continuity"
        ):
            raise ValueError(
                "shared_surface_restore_entries must match shared_surface_restore_continuity count."
            )

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_display_restore_continuity_contract() -> DisplayRestoreContinuityContract:
    """Build canonical display restore continuity contract."""
    restore_contract = build_display_assignment_restore_contract()

    entries = tuple(
        DisplayRestoreContinuityEntry(
            continuity_id=f"display_restore_continuity_{index:03d}",
            assignment_id=entry.assignment_id,
            display_target_id=entry.display_target_id,
            restore_continuity_state="restore_continuity_preserved",
            restore_continuity_class=(
                "shared_surface_restore_continuity"
                if entry.restore_decision == "restore_shared_surface"
                else "direct_restore_continuity"
            ),
            workspace_id=entry.workspace_id,
            operator_visible=True,
            description=(
                f"Canonical restore continuity entry for {entry.assignment_id}."
            ),
        )
        for index, entry in enumerate(restore_contract.entries, start=1)
    )

    return DisplayRestoreContinuityContract(
        contract_id="display_restore_continuity_contract_001",
        total_entries=len(entries),
        direct_restore_entries=sum(
            1
            for entry in entries
            if entry.restore_continuity_class == "direct_restore_continuity"
        ),
        shared_surface_restore_entries=sum(
            1
            for entry in entries
            if entry.restore_continuity_class == "shared_surface_restore_continuity"
        ),
        operator_visible_entries=sum(1 for entry in entries if entry.operator_visible),
        entries=entries,
    )
