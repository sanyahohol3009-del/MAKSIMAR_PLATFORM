from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.display_target_vocabulary_contract import (
    build_display_target_vocabulary_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.physical_monitor_identity_contract import (
    build_physical_monitor_identity_contract,
)


LogicalDisplayTargetState = Literal[
    "logical_display_target_ready",
]

LogicalDisplayTargetClass = Literal[
    "foundation_primary_logical_target",
    "foundation_secondary_logical_target",
    "operator_interaction_logical_target",
]

ALL_LOGICAL_DISPLAY_TARGET_STATES: tuple[LogicalDisplayTargetState, ...] = (
    "logical_display_target_ready",
)

ALL_LOGICAL_DISPLAY_TARGET_CLASSES: tuple[LogicalDisplayTargetClass, ...] = (
    "foundation_primary_logical_target",
    "foundation_secondary_logical_target",
    "operator_interaction_logical_target",
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class LogicalDisplayTargetEntry:
    """Canonical logical display target entry."""

    logical_target_id: str
    display_target_id: str
    physical_monitor_id: str
    logical_target_state: LogicalDisplayTargetState
    logical_target_class: LogicalDisplayTargetClass
    display_role: str
    display_zone: str
    fallback_display_target_id: str
    operator_visible: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.logical_target_id, "logical_target_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.physical_monitor_id, "physical_monitor_id")
        _require_non_empty(self.display_role, "display_role")
        _require_non_empty(self.display_zone, "display_zone")
        _require_non_empty(
            self.fallback_display_target_id, "fallback_display_target_id"
        )
        _require_non_empty(self.description, "description")

        if self.logical_target_state not in ALL_LOGICAL_DISPLAY_TARGET_STATES:
            raise ValueError(
                "logical_target_state must be one of "
                f"{ALL_LOGICAL_DISPLAY_TARGET_STATES}, got {self.logical_target_state!r}."
            )

        if self.logical_target_class not in ALL_LOGICAL_DISPLAY_TARGET_CLASSES:
            raise ValueError(
                "logical_target_class must be one of "
                f"{ALL_LOGICAL_DISPLAY_TARGET_CLASSES}, got {self.logical_target_class!r}."
            )

        if not self.operator_visible:
            raise ValueError(
                "operator_visible must remain true for canonical logical display targets."
            )


@dataclass(frozen=True, slots=True)
class LogicalDisplayTargetContract:
    """Canonical logical display target contract."""

    contract_id: str
    total_entries: int
    operator_visible_entries: int
    entries: tuple[LogicalDisplayTargetEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.operator_visible_entries != sum(
            1 for entry in self.entries if entry.operator_visible
        ):
            raise ValueError(
                "operator_visible_entries must match operator_visible count."
            )


def build_logical_display_target_contract() -> LogicalDisplayTargetContract:
    """Build canonical logical display target contract."""
    display_target_contract = build_display_target_vocabulary_contract()
    physical_identity_contract = build_physical_monitor_identity_contract()

    display_target_map = {
        entry.display_target_id: entry for entry in display_target_contract.entries
    }
    physical_identity_map = {
        entry.display_target_id: entry for entry in physical_identity_contract.entries
    }

    logical_class_map: dict[str, LogicalDisplayTargetClass] = {
        "display_foundation_primary": "foundation_primary_logical_target",
        "display_foundation_secondary": "foundation_secondary_logical_target",
        "display_operator_interaction": "operator_interaction_logical_target",
    }

    fallback_map = {
        "display_foundation_primary": "display_foundation_secondary",
        "display_foundation_secondary": "display_foundation_primary",
        "display_operator_interaction": "display_operator_interaction",
    }

    ordered_display_targets = (
        "display_foundation_primary",
        "display_foundation_secondary",
        "display_operator_interaction",
    )

    entries = tuple(
        LogicalDisplayTargetEntry(
            logical_target_id=f"logical_display_target_{index:03d}",
            display_target_id=display_target_id,
            physical_monitor_id=physical_identity_map[
                display_target_id
            ].physical_monitor_id,
            logical_target_state="logical_display_target_ready",
            logical_target_class=logical_class_map[display_target_id],
            display_role=display_target_map[display_target_id].display_role,
            display_zone=display_target_map[display_target_id].display_zone,
            fallback_display_target_id=fallback_map[display_target_id],
            operator_visible=True,
            description=(
                f"Canonical logical display target entry for {display_target_id}."
            ),
        )
        for index, display_target_id in enumerate(ordered_display_targets, start=1)
    )

    return LogicalDisplayTargetContract(
        contract_id="logical_display_target_contract_001",
        total_entries=len(entries),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )
